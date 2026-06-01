"""
courses.py — Course catalogue, enrolment, materials, and attendance.

GET    /api/courses/                     List all courses
POST   /api/courses/                     Create course (teacher/admin)
GET    /api/courses/{id}                 Course detail + student list
PUT    /api/courses/{id}                 Update course metadata
DELETE /api/courses/{id}                 Delete course
POST   /api/courses/{id}/enroll          Student self-enrols
DELETE /api/courses/{id}/enroll          Student unenrols
GET    /api/courses/{id}/materials       List materials
POST   /api/courses/{id}/materials       Add material (own teacher/admin)
DELETE /api/courses/{id}/materials/{mid} Remove material
POST   /api/courses/{id}/attendance      Record attendance batch
GET    /api/courses/{id}/attendance      Retrieve attendance records
POST   /api/courses/{id}/duplicate       Clone course with all content
"""
import os
import uuid
import mimetypes
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from database import get_db
import models
import security

# ── Upload directory ──────────────────────────────────────────────────────────
_UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads/materials"))
_MAX_MB = int(os.getenv("MAX_UPLOAD_MB", "200"))

def _ensure_upload_dir() -> Path:
    _UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return _UPLOAD_DIR

router = APIRouter()


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    subject: Optional[str] = None
    grade_level: Optional[str] = None


class MaterialCreate(BaseModel):
    title: str
    content: Optional[str] = None
    url: Optional[str] = None


class AttendanceRecord(BaseModel):
    student_id: int
    status: str


class AttendanceBatch(BaseModel):
    date: date
    records: List[AttendanceRecord]


@router.get("/")
def list_courses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    courses = db.query(models.Course).all()
    enrolled_ids = set()
    if current_user.role == "student":
        enrolled_ids = {
            e.course_id
            for e in db.query(models.Enrollment)
            .filter(models.Enrollment.student_id == current_user.id)
            .all()
        }
    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "subject": c.subject,
            "grade_level": c.grade_level,
            "teacher_id": c.teacher_id,
            "teacher_name": c.teacher.name if c.teacher else None,
            "enrolled": c.id in enrolled_ids,
            "student_count": len(c.enrollments),
        }
        for c in courses
    ]


@router.post("/")
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    course = models.Course(
        title=data.title,
        description=data.description,
        subject=data.subject,
        grade_level=data.grade_level,
        teacher_id=current_user.id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return {"id": course.id, "title": course.title}


@router.get("/{course_id}")
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    enrolled = False
    if current_user.role == "student":
        enrolled = (
            db.query(models.Enrollment)
            .filter(
                models.Enrollment.course_id == course_id,
                models.Enrollment.student_id == current_user.id,
            )
            .first()
            is not None
        )
    # Only the course's own teacher (or an admin) may see the enrolled student list.
    # Another teacher browsing the catalogue has no need to see student data.
    is_course_teacher = (
        current_user.role == "teacher" and course.teacher_id == current_user.id
    )
    students = []
    if current_user.role == "admin" or is_course_teacher:
        students = [
            {"id": e.student.id, "name": e.student.name, "email": e.student.email}
            for e in course.enrollments
        ]
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "subject": course.subject,
        "grade_level": course.grade_level,
        "teacher_id": course.teacher_id,
        "teacher_name": course.teacher.name if course.teacher else None,
        "enrolled": enrolled,
        "students": students,
    }


@router.put("/{course_id}")
def update_course(
    course_id: int,
    data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    if current_user.role == "teacher" and course.teacher_id != current_user.id:
        raise HTTPException(403, "Not your course")
    course.title = data.title
    course.description = data.description
    course.subject = data.subject
    course.grade_level = data.grade_level
    db.commit()
    return {"ok": True}


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    if current_user.role == "teacher" and course.teacher_id != current_user.id:
        raise HTTPException(403, "Not your course")
    db.delete(course)
    db.commit()
    return {"ok": True}


# Enrollment

@router.post("/{course_id}/enroll")
def enroll(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    if not db.query(models.Course).filter(models.Course.id == course_id).first():
        raise HTTPException(404, "Course not found")
    if (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.course_id == course_id,
            models.Enrollment.student_id == current_user.id,
        )
        .first()
    ):
        raise HTTPException(400, "Already enrolled")
    db.add(models.Enrollment(student_id=current_user.id, course_id=course_id))
    db.commit()
    return {"ok": True}


@router.delete("/{course_id}/enroll")
def unenroll(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    e = (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.course_id == course_id,
            models.Enrollment.student_id == current_user.id,
        )
        .first()
    )
    if not e:
        raise HTTPException(404, "Not enrolled")
    db.delete(e)
    db.commit()
    return {"ok": True}


# Materials

@router.get("/{course_id}/materials")
def list_materials(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    return [
        {
            "id": m.id,
            "title": m.title,
            "content": m.content,
            "url": m.url,
            # Infer type for legacy rows that pre-date the material_type column
            "material_type": m.material_type or ("link" if m.url else "text"),
            "file_name": m.file_name,
            "file_size": m.file_size,
            "file_mime": m.file_mime,
            "created_at": str(m.created_at),
        }
        for m in db.query(models.Material).filter(models.Material.course_id == course_id).all()
    ]


@router.post("/{course_id}/materials")
def add_material(
    course_id: int,
    data: MaterialCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    mat_type = "link" if data.url else "text"
    m = models.Material(
        course_id=course_id,
        title=data.title,
        content=data.content,
        url=data.url,
        material_type=mat_type,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return {"id": m.id, "title": m.title}


@router.post("/{course_id}/materials/upload")
async def upload_material(
    course_id: int,
    title: str = Form(...),
    file: UploadFile = FFile(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Upload a file (PDF, video, image, etc.) as course material."""
    security.require_course_access(course_id, current_user, db)
    upload_dir = _ensure_upload_dir()

    content = await file.read()
    if len(content) > _MAX_MB * 1024 * 1024:
        raise HTTPException(413, f"File too large — maximum {_MAX_MB} MB allowed.")

    original_name = file.filename or "upload"
    ext = Path(original_name).suffix.lower()
    if not ext and file.content_type:
        ext = mimetypes.guess_extension(file.content_type) or ""
    mime = file.content_type or mimetypes.guess_type(original_name)[0] or "application/octet-stream"

    stored_name = f"{uuid.uuid4()}{ext}"
    stored_path = upload_dir / stored_name
    stored_path.write_bytes(content)

    m = models.Material(
        course_id=course_id,
        title=title,
        material_type="file",
        file_name=original_name,
        file_path=str(stored_path),
        file_size=len(content),
        file_mime=mime,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return {"id": m.id, "title": m.title, "file_name": m.file_name}


@router.get("/{course_id}/materials/{material_id}/file")
def serve_material_file(
    course_id: int,
    material_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    """Serve an uploaded material file, checking course access."""
    m = db.query(models.Material).filter(
        models.Material.id == material_id,
        models.Material.course_id == course_id,
    ).first()
    if not m:
        raise HTTPException(404, "Material not found")
    if m.material_type != "file" or not m.file_path:
        raise HTTPException(400, "This material has no attached file")

    path = Path(m.file_path)
    if not path.exists():
        raise HTTPException(404, "File not found on server")

    # Access control
    if current_user.role == "student":
        enrolled = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == course_id,
            models.Enrollment.student_id == current_user.id,
        ).first()
        if not enrolled:
            raise HTTPException(403, "You are not enrolled in this course")
    elif current_user.role == "teacher":
        security.require_course_access(course_id, current_user, db)
    # admin: always allowed

    mime = m.file_mime or "application/octet-stream"
    viewable = (
        mime.startswith(("image/", "video/", "audio/", "text/"))
        or mime == "application/pdf"
    )
    disposition = "inline" if viewable else "attachment"
    safe_name = (m.file_name or "download").replace('"', "'")

    return FileResponse(
        path=str(path),
        media_type=mime,
        headers={"Content-Disposition": f'{disposition}; filename="{safe_name}"'},
    )


@router.delete("/{course_id}/materials/{material_id}")
def delete_material(
    course_id: int,
    material_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    m = db.query(models.Material).filter(
        models.Material.id == material_id, models.Material.course_id == course_id
    ).first()
    if not m:
        raise HTTPException(404, "Material not found")
    # Remove uploaded file from disk if present
    if m.file_path:
        try:
            Path(m.file_path).unlink(missing_ok=True)
        except Exception:
            pass
    db.delete(m)
    db.commit()
    return {"ok": True}


# Attendance

@router.post("/{course_id}/attendance")
def mark_attendance(
    course_id: int,
    data: AttendanceBatch,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    for rec in data.records:
        existing = db.query(models.Attendance).filter(
            models.Attendance.course_id == course_id,
            models.Attendance.student_id == rec.student_id,
            models.Attendance.date == data.date,
        ).first()
        if existing:
            existing.status = rec.status
        else:
            db.add(models.Attendance(
                course_id=course_id,
                student_id=rec.student_id,
                date=data.date,
                status=rec.status,
            ))
    db.commit()
    return {"ok": True}


@router.get("/{course_id}/attendance")
def get_attendance(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    records = db.query(models.Attendance).filter(models.Attendance.course_id == course_id).all()
    return [{"student_id": r.student_id, "date": str(r.date), "status": r.status} for r in records]


@router.post("/{course_id}/duplicate")
def duplicate_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Duplicate a full course — copies assignments, materials, quizzes, sessions."""
    source = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not source:
        raise HTTPException(404, "Course not found")
    security.require_course_access(course_id, current_user, db)

    new_course = models.Course(
        title=source.title + " (Copy)",
        description=source.description,
        subject=source.subject,
        grade_level=source.grade_level,
        teacher_id=current_user.id,
    )
    db.add(new_course)
    db.flush()

    # Copy materials
    for m in source.materials:
        db.add(models.Material(
            course_id=new_course.id,
            title=m.title,
            content=m.content,
            url=m.url,
        ))

    # Copy assignments
    for a in source.assignments:
        db.add(models.Assignment(
            course_id=new_course.id,
            title=a.title,
            description=a.description,
            due_date=a.due_date,
            max_score=a.max_score,
            is_extra_credit=a.is_extra_credit,
        ))

    # Copy sessions
    for s in source.sessions:
        db.add(models.ClassSession(
            course_id=new_course.id,
            title=s.title,
            session_type=s.session_type,
            date=s.date,
            duration_minutes=s.duration_minutes,
            location=s.location,
            notes=s.notes,
        ))

    # Copy quizzes + questions + options
    for q in source.quizzes:
        new_q = models.Quiz(
            course_id=new_course.id,
            title=q.title,
            description=q.description,
            time_limit=q.time_limit,
            due_date=q.due_date,
            shuffle=q.shuffle,
            is_published=False,  # copies always start as draft
        )
        db.add(new_q)
        db.flush()
        for qq in q.questions:
            new_qq = models.QuizQuestion(
                quiz_id=new_q.id,
                question_text=qq.question_text,
                question_type=qq.question_type,
                points=qq.points,
                order_num=qq.order_num,
            )
            db.add(new_qq)
            db.flush()
            for opt in qq.options:
                db.add(models.QuizOption(
                    question_id=new_qq.id,
                    option_text=opt.option_text,
                    is_correct=opt.is_correct,
                ))

    db.commit()
    db.refresh(new_course)
    return {"id": new_course.id, "title": new_course.title, "ok": True}
