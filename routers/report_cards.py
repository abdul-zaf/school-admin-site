"""
report_cards.py — AI-generated student report cards with teacher publish control.

POST   /api/report-cards/generate                      Generate AI report card (teacher)
GET    /api/report-cards/course/{course_id}             List all report cards for a course (teacher)
GET    /api/report-cards/course/{course_id}/student/{student_id}  Get a specific card (teacher/student — student only sees published)
PUT    /api/report-cards/{id}                          Edit content (teacher)
POST   /api/report-cards/{id}/publish                  Publish card (teacher)
POST   /api/report-cards/{id}/unpublish                Unpublish card (teacher)
DELETE /api/report-cards/{id}                          Delete card (teacher)
GET    /api/report-cards/my                            Student: list all my published report cards
"""
import sys
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
import security
from database import get_db
from services.ollama import chat as ollama_chat, OLLAMA_MODEL

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    course_id: int
    student_id: int

class EditRequest(BaseModel):
    content: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _serialize(rc: models.ReportCard) -> dict:
    return {
        "id": rc.id,
        "student_id": rc.student_id,
        "student_name": rc.student.name if rc.student else None,
        "course_id": rc.course_id,
        "course_title": rc.course.title if rc.course else None,
        "teacher_id": rc.teacher_id,
        "content": rc.content,
        "is_published": rc.is_published,
        "created_at": str(rc.created_at),
        "updated_at": str(rc.updated_at),
    }


def _build_student_summary(student_id: int, course_id: int, db: Session) -> str:
    """Gather all available data for one student in one course and return a text summary."""
    student = db.query(models.User).filter(models.User.id == student_id).first()
    course  = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not student or not course:
        return ""

    lines = [
        f"Student: {student.name}",
        f"Course: {course.title}",
        "",
    ]

    # ── Assignments & grades ──────────────────────────────────────────────────
    assignments = db.query(models.Assignment).filter(
        models.Assignment.course_id == course_id
    ).order_by(models.Assignment.due_date).all()

    if assignments:
        lines.append("=== Assignments ===")
        for a in assignments:
            sub = db.query(models.Submission).filter(
                models.Submission.assignment_id == a.id,
                models.Submission.student_id == student_id,
            ).first()
            if sub:
                if sub.score is not None:
                    pct = round(sub.score / a.max_score * 100) if a.max_score else 0
                    lines.append(f"  {a.title}: {sub.score}/{a.max_score} ({pct}%)")
                else:
                    lines.append(f"  {a.title}: submitted, not yet graded")
            else:
                lines.append(f"  {a.title}: not submitted (max {a.max_score})")
        lines.append("")

    # ── Quizzes ───────────────────────────────────────────────────────────────
    quizzes = db.query(models.Quiz).filter(
        models.Quiz.course_id == course_id,
        models.Quiz.is_published == True,
    ).all()

    if quizzes:
        lines.append("=== Quizzes / Exams ===")
        for q in quizzes:
            attempt = db.query(models.QuizAttempt).filter(
                models.QuizAttempt.quiz_id == q.id,
                models.QuizAttempt.student_id == student_id,
            ).order_by(models.QuizAttempt.started_at.desc()).first()
            label = "Exam" if getattr(q, "is_exam", False) else "Quiz"
            if attempt and attempt.score is not None:
                pct = round(attempt.score / attempt.max_score * 100) if attempt.max_score else 0
                lines.append(f"  [{label}] {q.title}: {attempt.score}/{attempt.max_score} ({pct}%)")
            elif attempt:
                lines.append(f"  [{label}] {q.title}: attempted, score pending")
            else:
                lines.append(f"  [{label}] {q.title}: not attempted")
        lines.append("")

    # ── Attendance ────────────────────────────────────────────────────────────
    att_records = db.query(models.Attendance).filter(
        models.Attendance.course_id == course_id,
        models.Attendance.student_id == student_id,
    ).all()

    if att_records:
        total   = len(att_records)
        present = sum(1 for r in att_records if r.status == "present")
        late    = sum(1 for r in att_records if r.status == "late")
        absent  = sum(1 for r in att_records if r.status == "absent")
        pct     = round(present / total * 100) if total else 0
        lines.append("=== Attendance ===")
        lines.append(f"  Total classes recorded: {total}")
        lines.append(f"  Present: {present} | Late: {late} | Absent: {absent}")
        lines.append(f"  Attendance rate: {pct}%")
        lines.append("")

    # ── Module completions ────────────────────────────────────────────────────
    modules = db.query(models.CourseModule).filter(
        models.CourseModule.course_id == course_id
    ).all()

    if modules:
        lines.append("=== Course Modules ===")
        for mod in modules:
            items = db.query(models.ModuleItem).filter(
                models.ModuleItem.module_id == mod.id
            ).all()
            completed = db.query(models.ModuleCompletion).filter(
                models.ModuleCompletion.student_id == student_id,
                models.ModuleCompletion.module_item_id.in_([i.id for i in items]),
            ).count() if items else 0
            lines.append(f"  {mod.title}: {completed}/{len(items)} items completed")
        lines.append("")

    # ── XP ────────────────────────────────────────────────────────────────────
    xp_row = db.query(models.UserXP).filter(models.UserXP.user_id == student_id).first()
    if xp_row:
        lines.append(f"=== XP / Engagement ===")
        lines.append(f"  Total XP earned: {xp_row.total_xp}")
        lines.append("")

    return "\n".join(lines)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/generate")
def generate_report_card(
    data: GenerateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(data.course_id, current_user, db)

    student = db.query(models.User).filter(
        models.User.id == data.student_id,
        models.User.role == "student",
    ).first()
    if not student:
        raise HTTPException(404, "Student not found")

    enrolled = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == data.course_id,
        models.Enrollment.student_id == data.student_id,
    ).first()
    if not enrolled:
        raise HTTPException(400, "Student is not enrolled in this course")

    summary = _build_student_summary(data.student_id, data.course_id, db)
    if not summary.strip():
        raise HTTPException(400, "No data available to generate a report card")

    system_prompt = (
        "You are an experienced teacher writing a formal academic report card for a student. "
        "Use the data provided to write a structured, professional report card. "
        "Include: an overall performance summary, strengths observed, areas for improvement, "
        "attendance commentary, and a brief motivational closing remark. "
        "Use clear sections with headings. Be specific — cite actual scores and percentages from the data. "
        "Do not make up information not present in the data. Keep the tone professional and encouraging."
    )

    try:
        content = ollama_chat(
            [{"role": "user", "content": f"Please write a report card based on the following student data:\n\n{summary}"}],
            system=system_prompt,
            temperature=0.4,
            max_tokens=2048,
        )
    except Exception as exc:
        print(f"[ReportCard] Ollama error: {exc}", file=sys.stderr)
        raise HTTPException(503, f"AI service unavailable: {exc}")

    # Overwrite any existing draft for this student/course (keep one card per student per course)
    existing = db.query(models.ReportCard).filter(
        models.ReportCard.course_id == data.course_id,
        models.ReportCard.student_id == data.student_id,
    ).first()

    if existing:
        existing.content    = content
        existing.teacher_id = current_user.id
        existing.is_published = False
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return _serialize(existing)

    rc = models.ReportCard(
        student_id  = data.student_id,
        course_id   = data.course_id,
        teacher_id  = current_user.id,
        content     = content,
        is_published= False,
    )
    db.add(rc)
    db.commit()
    db.refresh(rc)
    return _serialize(rc)


@router.get("/my")
def my_report_cards(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    cards = db.query(models.ReportCard).filter(
        models.ReportCard.student_id == current_user.id,
        models.ReportCard.is_published == True,
    ).order_by(models.ReportCard.updated_at.desc()).all()
    return [_serialize(rc) for rc in cards]


@router.get("/course/{course_id}")
def list_course_report_cards(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    cards = db.query(models.ReportCard).filter(
        models.ReportCard.course_id == course_id,
    ).order_by(models.ReportCard.student_id).all()
    return [_serialize(rc) for rc in cards]


@router.get("/course/{course_id}/student/{student_id}")
def get_report_card(
    course_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    rc = db.query(models.ReportCard).filter(
        models.ReportCard.course_id  == course_id,
        models.ReportCard.student_id == student_id,
    ).first()
    if not rc:
        raise HTTPException(404, "Report card not found")
    if current_user.role == "student":
        if current_user.id != student_id:
            raise HTTPException(403, "Access denied")
        if not rc.is_published:
            raise HTTPException(404, "Report card not available")
    elif current_user.role == "teacher":
        security.require_course_access(course_id, current_user, db)
    return _serialize(rc)


@router.put("/{rc_id}")
def edit_report_card(
    rc_id: int,
    data: EditRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    rc = db.query(models.ReportCard).filter(models.ReportCard.id == rc_id).first()
    if not rc:
        raise HTTPException(404, "Report card not found")
    security.require_course_access(rc.course_id, current_user, db)
    rc.content    = data.content
    rc.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(rc)
    return _serialize(rc)


@router.post("/{rc_id}/publish")
def publish_report_card(
    rc_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    rc = db.query(models.ReportCard).filter(models.ReportCard.id == rc_id).first()
    if not rc:
        raise HTTPException(404, "Report card not found")
    security.require_course_access(rc.course_id, current_user, db)
    rc.is_published = True
    rc.updated_at   = datetime.utcnow()
    db.commit()
    return {"ok": True, "is_published": True}


@router.post("/{rc_id}/unpublish")
def unpublish_report_card(
    rc_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    rc = db.query(models.ReportCard).filter(models.ReportCard.id == rc_id).first()
    if not rc:
        raise HTTPException(404, "Report card not found")
    security.require_course_access(rc.course_id, current_user, db)
    rc.is_published = False
    rc.updated_at   = datetime.utcnow()
    db.commit()
    return {"ok": True, "is_published": False}


@router.delete("/{rc_id}")
def delete_report_card(
    rc_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    rc = db.query(models.ReportCard).filter(models.ReportCard.id == rc_id).first()
    if not rc:
        raise HTTPException(404, "Report card not found")
    security.require_course_access(rc.course_id, current_user, db)
    db.delete(rc)
    db.commit()
    return {"ok": True}
