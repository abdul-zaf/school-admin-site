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
import uuid
import mimetypes
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File as FFile, Form
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models
import security
from services.email import send_grade_notification
from services.knowledge_base import index_assignment
from routers.notifications import notify as push_notif

_UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads/submissions"))
_MAX_MB = int(os.getenv("MAX_UPLOAD_MB", "200"))

def _ensure_upload_dir() -> Path:
    _UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return _UPLOAD_DIR

router = APIRouter()


class AssignmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: float = 100.0
    late_penalty_per_day: float = 0.0
    max_late_days: Optional[int] = None
    allow_resubmission: bool = False
    max_submissions: int = 1


class AssignmentEdit(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: float = 100.0
    late_penalty_per_day: float = 0.0
    max_late_days: Optional[int] = None
    allow_resubmission: bool = False
    max_submissions: int = 1


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

    # For students, build the set of completed material ids once
    completed_material_ids: set = set()
    if current_user.role == "student":
        comps = db.query(models.MaterialCompletion).filter(
            models.MaterialCompletion.student_id == current_user.id,
        ).all()
        completed_material_ids = {c.material_id for c in comps}

    result = []
    for a in assignments:
        # Hide material-gated assignments from students who haven't completed the material
        if current_user.role == "student" and a.unlock_material_id:
            if a.unlock_material_id not in completed_material_ids:
                continue

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
        late_penalty_per_day=data.late_penalty_per_day,
        max_late_days=data.max_late_days,
        allow_resubmission=data.allow_resubmission,
        max_submissions=data.max_submissions,
    )
    db.add(a)
    db.flush()
    index_assignment(db, a)   # ← auto-index description for AI tutor KB
    db.commit()
    db.refresh(a)

    # Notify enrolled students
    due_str = f" — due {a.due_date.strftime('%d %b')}" if a.due_date else ""
    enrollments = db.query(models.Enrollment).filter(models.Enrollment.course_id == course_id).all()
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    course_title = course.title if course else "your course"
    for enr in enrollments:
        push_notif(db, enr.student_id, "assignment",
                   f"📋 New assignment: {a.title}",
                   f"{course_title}{due_str}",
                   link=f"assignment:{a.id}")
    db.commit()

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

    # Students cannot access material-gated assignments until they complete the material
    if current_user.role == "student" and a.unlock_material_id:
        completed = db.query(models.MaterialCompletion).filter(
            models.MaterialCompletion.student_id == current_user.id,
            models.MaterialCompletion.material_id == a.unlock_material_id,
        ).first()
        if not completed:
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
                "file_name": s.file_name,
                "file_mime": s.file_mime,
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
                "file_name": s.file_name,
                "file_mime": s.file_mime,
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
        "late_penalty_per_day": a.late_penalty_per_day,
        "max_late_days": a.max_late_days,
        "allow_resubmission": a.allow_resubmission,
        "max_submissions": a.max_submissions,
        "created_at": str(a.created_at),
        "submissions": submissions,
        "my_submission": my_sub,
    }


@router.put("/{assignment_id}")
def edit_assignment(
    assignment_id: int,
    data: AssignmentEdit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    a = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not a:
        raise HTTPException(404, "Assignment not found")
    security.require_course_access(a.course_id, current_user, db)
    a.title = data.title
    a.description = data.description
    a.due_date = data.due_date
    a.max_score = data.max_score
    a.late_penalty_per_day = data.late_penalty_per_day
    a.max_late_days = data.max_late_days
    a.allow_resubmission = data.allow_resubmission
    a.max_submissions = data.max_submissions
    db.commit()
    db.refresh(a)
    return {
        "id": a.id,
        "title": a.title,
        "description": a.description,
        "due_date": str(a.due_date) if a.due_date else None,
        "max_score": a.max_score,
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
async def submit_assignment(
    assignment_id: int,
    content: str = Form(""),
    file: Optional[UploadFile] = FFile(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(404, "Assignment not found")

    if not content.strip() and (file is None or not file.filename):
        raise HTTPException(400, "Submission must include text or a file.")

    # Check late submission policy
    now = datetime.utcnow()
    if assignment.due_date and now > assignment.due_date:
        days_late = (now - assignment.due_date).days
        if assignment.max_late_days is not None and days_late > assignment.max_late_days:
            raise HTTPException(400, f"Submission deadline passed. Maximum {assignment.max_late_days} late day(s) allowed.")

    # Handle file upload
    stored_file_name = stored_file_path = stored_file_mime = None
    stored_file_size = None
    if file and file.filename:
        file_bytes = await file.read()
        if len(file_bytes) > _MAX_MB * 1024 * 1024:
            raise HTTPException(413, f"File too large — maximum {_MAX_MB} MB allowed.")
        upload_dir = _ensure_upload_dir()
        ext = Path(file.filename).suffix.lower()
        if not ext and file.content_type:
            ext = mimetypes.guess_extension(file.content_type) or ""
        stored_file_mime = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
        stored_name = f"{uuid.uuid4()}{ext}"
        stored_path = upload_dir / stored_name
        stored_path.write_bytes(file_bytes)
        stored_file_name = file.filename
        stored_file_path = str(stored_path)
        stored_file_size = len(file_bytes)

    # Count existing submissions for resubmission check
    existing_subs = db.query(models.Submission).filter(
        models.Submission.assignment_id == assignment_id,
        models.Submission.student_id == current_user.id,
    ).all()

    if existing_subs:
        existing = existing_subs[0]
        if not assignment.allow_resubmission:
            raise HTTPException(400, "Resubmission is not allowed for this assignment")
        if assignment.max_submissions > 1 and len(existing_subs) >= assignment.max_submissions:
            raise HTTPException(400, f"Maximum submissions ({assignment.max_submissions}) reached")
        # Delete old file if replaced
        if stored_file_path and existing.file_path:
            try: Path(existing.file_path).unlink(missing_ok=True)
            except Exception: pass
        existing.content = content
        if stored_file_path:
            existing.file_name = stored_file_name
            existing.file_path = stored_file_path
            existing.file_mime = stored_file_mime
            existing.file_size = stored_file_size
        existing.submitted_at = now
        db.commit()
        try:
            from routers.streaks import record_activity
            from routers.xp import award_xp
            from routers.notifications import notify
            record_activity(db, current_user.id)
            award_xp(db, current_user.id, "submit_assignment", f"Resubmitted: {assignment.title}")
            course = db.query(models.Course).filter(models.Course.id == assignment.course_id).first()
            if course:
                notify(db, course.teacher_id, "submission",
                       f"{current_user.name} resubmitted an assignment",
                       f'"{assignment.title}" in {course.title}',
                       f"gradebook?course_id={course.id}&student_id={current_user.id}")
            db.commit()
        except Exception:
            pass
        return {"id": existing.id, "resubmitted": True}

    s = models.Submission(
        assignment_id=assignment_id,
        student_id=current_user.id,
        content=content,
        file_name=stored_file_name,
        file_path=stored_file_path,
        file_mime=stored_file_mime,
        file_size=stored_file_size,
    )
    db.add(s)
    db.commit()
    db.refresh(s)

    try:
        from routers.streaks import record_activity
        from routers.xp import award_xp
        from routers.notifications import notify
        record_activity(db, current_user.id)
        award_xp(db, current_user.id, "submit_assignment", f"Submitted: {assignment.title}")
        course = db.query(models.Course).filter(models.Course.id == assignment.course_id).first()
        if course:
            notify(db, course.teacher_id, "submission",
                   f"{current_user.name} submitted an assignment",
                   f'"{assignment.title}" in {course.title}',
                   f"gradebook?course_id={course.id}&student_id={current_user.id}")
        db.commit()
    except Exception:
        pass

    return {"id": s.id, "submitted": True}


@router.get("/submissions/{submission_id}/file")
def serve_submission_file(
    submission_id: int,
    dl_token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user_optional),
):
    user = current_user
    if user is None:
        if not dl_token:
            raise HTTPException(401, "Authentication required")
        user = security.get_user_from_token(dl_token, db)
    if user is None:
        raise HTTPException(401, "Invalid token")

    s = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not s:
        raise HTTPException(404, "Submission not found")

    # Students can only download their own submission; teachers/admins can download any
    if user.role == "student" and s.student_id != user.id:
        raise HTTPException(403, "Forbidden")
    if user.role == "teacher":
        security.require_course_access(s.assignment.course_id, user, db)

    if not s.file_path:
        raise HTTPException(404, "No file attached to this submission")

    path = Path(s.file_path)
    if not path.exists():
        raise HTTPException(404, "File not found on server")

    return FileResponse(
        path=str(path),
        media_type=s.file_mime or "application/octet-stream",
        filename=s.file_name or path.name,
    )


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

    # Apply late penalty if applicable
    final_score = data.score
    late_note = ""
    assignment = s.assignment
    if assignment.due_date and s.submitted_at and s.submitted_at > assignment.due_date:
        if assignment.late_penalty_per_day and assignment.late_penalty_per_day > 0:
            days_late = max(0, (s.submitted_at - assignment.due_date).days)
            penalty_pct = min(days_late * assignment.late_penalty_per_day, 100.0)
            penalty = data.score * (penalty_pct / 100.0)
            final_score = max(0.0, data.score - penalty)
            late_note = f" (Late penalty applied: -{penalty_pct:.0f}% = -{penalty:.1f} pts)"

    s.score = final_score
    s.feedback = (data.feedback or "") + late_note
    s.graded_at = datetime.utcnow()
    gc = models.GradeChange(
        submission_id=submission_id,
        changed_by=current_user.id,
        old_score=old_score,
        new_score=final_score,
        reason=(data.feedback or "") + late_note,
    )
    db.add(gc)
    db.commit()
    # Email the student (non-blocking)
    student = s.student
    if getattr(student, "email_notifications", True):
        app_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("APP_URL") or ""
        background_tasks.add_task(
            send_grade_notification,
            student.email,
            student.name,
            assignment.title,
            assignment.course.title,
            final_score,
            assignment.max_score,
            s.feedback,
            app_url,
        )
    return {"ok": True, "final_score": final_score}


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
