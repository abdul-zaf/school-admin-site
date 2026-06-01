"""
assignments.py — Assignment lifecycle: create, submit, grade.

GET    /api/assignments/course/{id}               List assignments for a course
POST   /api/assignments/course/{id}               Create assignment (teacher/admin)
GET    /api/assignments/{id}                      Get assignment + submissions
DELETE /api/assignments/{id}                      Delete (teacher/admin, own course)
POST   /api/assignments/{id}/submit               Student submits work
PUT    /api/assignments/submissions/{id}/grade    Grade a submission; emails student
GET    /api/assignments/submissions/{id}/grade-history  Audit trail of grade changes
"""
import os
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models
import security
from services.email import send_grade_notification

router = APIRouter()


class AssignmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: float = 100.0


class SubmissionCreate(BaseModel):
    content: str


class GradeSubmission(BaseModel):
    score: float
    feedback: Optional[str] = None


@router.get("/course/{course_id}")
def list_assignments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    assignments = db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()
    result = []
    for a in assignments:
        my_sub = None
        if current_user.role == "student":
            s = db.query(models.Submission).filter(
                models.Submission.assignment_id == a.id,
                models.Submission.student_id == current_user.id,
            ).first()
            if s:
                my_sub = {
                    "id": s.id,
                    "submitted_at": str(s.submitted_at),
                    "score": s.score,
                    "feedback": s.feedback,
                }
        result.append({
            "id": a.id,
            "course_id": a.course_id,
            "title": a.title,
            "description": a.description,
            "due_date": str(a.due_date) if a.due_date else None,
            "max_score": a.max_score,
            "created_at": str(a.created_at),
            "submission_count": len(a.submissions) if current_user.role in ("admin", "teacher") else None,
            "my_submission": my_sub,
        })
    return result


@router.post("/course/{course_id}")
def create_assignment(
    course_id: int,
    data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    a = models.Assignment(
        course_id=course_id,
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        max_score=data.max_score,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return {"id": a.id, "title": a.title}


@router.get("/{assignment_id}")
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    a = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not a:
        raise HTTPException(404, "Assignment not found")

    submissions = []
    if current_user.role in ("admin", "teacher"):
        # Only the course's own teacher (or admin) may see student submissions
        security.require_course_access(a.course_id, current_user, db)
        submissions = [
            {
                "id": s.id,
                "student_id": s.student_id,
                "student_name": s.student.name,
                "content": s.content,
                "score": s.score,
                "feedback": s.feedback,
                "submitted_at": str(s.submitted_at),
                "graded_at": str(s.graded_at) if s.graded_at else None,
            }
            for s in a.submissions
        ]

    my_sub = None
    if current_user.role == "student":
        s = db.query(models.Submission).filter(
            models.Submission.assignment_id == assignment_id,
            models.Submission.student_id == current_user.id,
        ).first()
        if s:
            my_sub = {
                "id": s.id,
                "content": s.content,
                "score": s.score,
                "feedback": s.feedback,
                "submitted_at": str(s.submitted_at),
            }

    return {
        "id": a.id,
        "course_id": a.course_id,
        "title": a.title,
        "description": a.description,
        "due_date": str(a.due_date) if a.due_date else None,
        "max_score": a.max_score,
        "created_at": str(a.created_at),
        "submissions": submissions,
        "my_submission": my_sub,
    }


@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    a = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not a:
        raise HTTPException(404, "Assignment not found")
    security.require_course_access(a.course_id, current_user, db)
    db.delete(a)
    db.commit()
    return {"ok": True}


@router.post("/{assignment_id}/submit")
def submit_assignment(
    assignment_id: int,
    data: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    if not db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first():
        raise HTTPException(404, "Assignment not found")
    existing = db.query(models.Submission).filter(
        models.Submission.assignment_id == assignment_id,
        models.Submission.student_id == current_user.id,
    ).first()
    if existing:
        existing.content = data.content
        existing.submitted_at = datetime.utcnow()
        db.commit()
        return {"id": existing.id, "resubmitted": True}
    s = models.Submission(
        assignment_id=assignment_id, student_id=current_user.id, content=data.content
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id, "submitted": True}


@router.put("/submissions/{submission_id}/grade")
def grade_submission(
    submission_id: int,
    data: GradeSubmission,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    s = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not s:
        raise HTTPException(404, "Submission not found")
    security.require_course_access(s.assignment.course_id, current_user, db)
    old_score = s.score
    s.score = data.score
    s.feedback = data.feedback
    s.graded_at = datetime.utcnow()
    gc = models.GradeChange(
        submission_id=submission_id,
        changed_by=current_user.id,
        old_score=old_score,
        new_score=data.score,
        reason=data.feedback or "",
    )
    db.add(gc)
    db.commit()
    # Email the student (non-blocking)
    app_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("APP_URL") or ""
    background_tasks.add_task(
        send_grade_notification,
        s.student.email,
        s.student.name,
        s.assignment.title,
        s.assignment.course.title,
        data.score,
        s.assignment.max_score,
        data.feedback,
        app_url,
    )
    return {"ok": True}


@router.get("/submissions/{submission_id}/grade-history")
def grade_history(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    s = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not s:
        raise HTTPException(404, "Submission not found")
    security.require_course_access(s.assignment.course_id, current_user, db)
    changes = db.query(models.GradeChange).filter(
        models.GradeChange.submission_id == submission_id
    ).order_by(models.GradeChange.changed_at.desc()).all()
    return [
        {
            "id": gc.id,
            "old_score": gc.old_score,
            "new_score": gc.new_score,
            "reason": gc.reason,
            "changed_by": gc.changer.name if gc.changer else "?",
            "changed_at": str(gc.changed_at),
        }
        for gc in changes
    ]
