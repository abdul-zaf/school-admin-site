"""
courses.py — Course catalogue, enrolment, materials, and attendance.

GET    /api/courses/                     List all courses
POST   /api/courses/                     Create course (teacher/admin)
GET    /api/courses/{id}                 Course detail + student list
GET    /api/courses/{id}/students        Enrolled student list (teacher/admin)
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
import sys
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File as FFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from database import get_db, SessionLocal
import models
import security
from services.knowledge_base import index_material, remove_material_index

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
    section_number: Optional[str] = None
    enrollment_cap: Optional[int] = None   # None = unlimited


class MaterialCreate(BaseModel):
    title: str
    content: Optional[str] = None
    url: Optional[str] = None
    unlock_quiz_id: Optional[int] = None


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
            "section_number": c.section_number,
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
        section_number=data.section_number,
        teacher_id=current_user.id,
        enrollment_cap=data.enrollment_cap,
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
        "section_number": course.section_number,
        "teacher_id": course.teacher_id,
        "teacher_name": course.teacher.name if course.teacher else None,
        "enrolled": enrolled,
        "students": students,
    }


@router.get("/{course_id}/students")
def list_course_students(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    if current_user.role == "teacher" and course.teacher_id != current_user.id:
        raise HTTPException(403, "Not your course")
    return [
        {"id": e.student.id, "name": e.student.name, "email": e.student.email}
        for e in course.enrollments
    ]


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
    course.section_number = data.section_number
    course.enrollment_cap = data.enrollment_cap
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

    # ── Pre-deletion cleanup ───────────────────────────────────────────────────
    # SQLAlchemy cascade-deletes both GradeCategory and Assignment from Course.
    # GradeCategory deletion tries to SET assignment.grade_category_id = NULL,
    # but those assignments are simultaneously being deleted — conflicting ops.
    # Null them out first to break the circular dependency.
    assignment_ids = [
        a.id for a in db.query(models.Assignment.id)
        .filter(models.Assignment.course_id == course_id).all()
    ]
    if assignment_ids:
        db.query(models.Assignment).filter(
            models.Assignment.course_id == course_id
        ).update({"grade_category_id": None, "rubric_id": None},
                 synchronize_session=False)

        # PeerReview has NOT NULL FKs to assignments and submissions — delete first
        submission_ids = [
            s.id for s in db.query(models.Submission.id)
            .filter(models.Submission.assignment_id.in_(assignment_ids)).all()
        ]
        if submission_ids:
            db.query(models.PeerReview).filter(
                models.PeerReview.reviewee_submission_id.in_(submission_ids)
            ).delete(synchronize_session=False)
        db.query(models.PeerReview).filter(
            models.PeerReview.assignment_id.in_(assignment_ids)
        ).delete(synchronize_session=False)

    # CoursePrerequisite rows reference courses.id via two columns — delete both directions
    db.query(models.CoursePrerequisite).filter(
        (models.CoursePrerequisite.course_id == course_id) |
        (models.CoursePrerequisite.prerequisite_course_id == course_id)
    ).delete(synchronize_session=False)

    # ModuleItem.item_type is an Enum; stale DB rows may have values not in the
    # current Enum definition (e.g. 'text'). Bulk-delete completions then items
    # before the ORM cascade so SQLAlchemy never tries to deserialise those rows.
    module_ids = [
        m.id for m in db.query(models.CourseModule.id)
        .filter(models.CourseModule.course_id == course_id).all()
    ]
    if module_ids:
        item_ids = [
            i.id for i in db.query(models.ModuleItem.id)
            .filter(models.ModuleItem.module_id.in_(module_ids)).all()
        ]
        if item_ids:
            db.query(models.ModuleCompletion).filter(
                models.ModuleCompletion.module_item_id.in_(item_ids)
            ).delete(synchronize_session=False)
        db.query(models.ModuleItem).filter(
            models.ModuleItem.module_id.in_(module_ids)
        ).delete(synchronize_session=False)

    db.flush()
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
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
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

    # Check prerequisites
    prereqs = db.query(models.CoursePrerequisite).filter(
        models.CoursePrerequisite.course_id == course_id
    ).all()
    for prereq in prereqs:
        # Student must have a graded submission (score >= 60%) in the prerequisite course
        assignments = db.query(models.Assignment).filter(
            models.Assignment.course_id == prereq.prerequisite_course_id
        ).all()
        if assignments:
            passed = False
            for a in assignments:
                sub = db.query(models.Submission).filter(
                    models.Submission.assignment_id == a.id,
                    models.Submission.student_id == current_user.id,
                    models.Submission.score != None,
                ).first()
                if sub and a.max_score and (sub.score / a.max_score * 100) >= 60:
                    passed = True
                    break
            if not passed:
                prereq_course = db.query(models.Course).filter(
                    models.Course.id == prereq.prerequisite_course_id
                ).first()
                prereq_title = prereq_course.title if prereq_course else str(prereq.prerequisite_course_id)
                raise HTTPException(
                    400,
                    f"Prerequisite not met: you must pass '{prereq_title}' (score >= 60%) before enrolling",
                )

    # Check enrollment cap
    if course.enrollment_cap is not None:
        current_count = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == course_id
        ).count()
        if current_count >= course.enrollment_cap:
            # Auto-add to waitlist
            already_waiting = db.query(models.EnrollmentWaitlist).filter(
                models.EnrollmentWaitlist.course_id == course_id,
                models.EnrollmentWaitlist.student_id == current_user.id,
            ).first()
            if not already_waiting:
                db.add(models.EnrollmentWaitlist(
                    course_id=course_id,
                    student_id=current_user.id,
                ))
                db.commit()
            raise HTTPException(
                400,
                f"Course is at capacity ({course.enrollment_cap} students). You have been added to the waitlist.",
            )

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
    db.flush()

    # Auto-promote the first waitlisted student
    first_waitlisted = (
        db.query(models.EnrollmentWaitlist)
        .filter(models.EnrollmentWaitlist.course_id == course_id)
        .order_by(models.EnrollmentWaitlist.joined_at)
        .first()
    )
    if first_waitlisted:
        db.add(models.Enrollment(
            student_id=first_waitlisted.student_id,
            course_id=course_id,
        ))
        db.delete(first_waitlisted)

    db.commit()
    return {"ok": True}


# Materials

@router.get("/{course_id}/materials")
def list_materials(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    mats = db.query(models.Material).filter(models.Material.course_id == course_id).all()
    # For students, build a set of completed material ids
    completed_ids: set = set()
    if current_user.role == "student":
        comps = db.query(models.MaterialCompletion).filter(
            models.MaterialCompletion.student_id == current_user.id,
            models.MaterialCompletion.material_id.in_([m.id for m in mats]),
        ).all()
        completed_ids = {c.material_id for c in comps}
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
            "unlock_quiz_id": m.unlock_quiz_id,
            "completed": m.id in completed_ids,
            "created_at": str(m.created_at),
        }
        for m in mats
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
        unlock_quiz_id=data.unlock_quiz_id,
    )
    db.add(m)
    db.flush()   # need m.id before indexing
    index_material(db, m)  # ← auto-index for AI tutor KB
    db.commit()
    db.refresh(m)
    return {"id": m.id, "title": m.title}


@router.post("/{course_id}/materials/upload")
async def upload_material(
    course_id: int,
    title: str = Form(...),
    file: UploadFile = FFile(...),
    unlock_quiz_id: Optional[int] = Form(None),
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
        unlock_quiz_id=unlock_quiz_id,
    )
    db.add(m)
    db.flush()   # need m.id before indexing
    index_material(db, m)  # ← auto-index for AI tutor KB (title + filename)
    db.commit()
    db.refresh(m)
    return {"id": m.id, "title": m.title, "file_name": m.file_name}


@router.get("/{course_id}/materials/{material_id}/file")
def serve_material_file(
    course_id: int,
    material_id: int,
    db: Session = Depends(get_db),
    # dl_token lets the browser open the URL directly (no custom headers needed).
    # Falls back to the standard Authorization header when dl_token is absent.
    dl_token: Optional[str] = None,
    current_user: models.User = Depends(security.get_current_user_optional),
):
    """Serve an uploaded material file with range-request support (streaming)."""
    # Resolve identity: prefer Authorization header; fall back to ?dl_token=
    user = current_user
    if user is None:
        if not dl_token:
            raise HTTPException(401, "Authentication required")
        user = security.get_user_from_token(dl_token, db)
        if user is None:
            raise HTTPException(401, "Invalid or expired token")

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
    if user.role == "student":
        enrolled = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == course_id,
            models.Enrollment.student_id == user.id,
        ).first()
        if not enrolled:
            raise HTTPException(403, "You are not enrolled in this course")
    elif user.role == "teacher":
        security.require_course_access(course_id, user, db)
    # admin: always allowed

    mime = m.file_mime or "application/octet-stream"
    viewable = (
        mime.startswith(("image/", "video/", "audio/", "text/"))
        or mime == "application/pdf"
    )
    disposition = "inline" if viewable else "attachment"
    safe_name = (m.file_name or "download").replace('"', "'")

    # FileResponse supports HTTP Range requests automatically — videos stream
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
    remove_material_index(db, m.id)  # ← remove from AI tutor KB
    db.delete(m)
    db.commit()
    return {"ok": True}


def _ai_generate_assignment_for_material(material_id: int, course_id: int, student_id: int) -> None:
    """Background task: generate an AI assignment from a completed material and notify the completing student."""
    db = SessionLocal()
    try:
        from services.ollama import chat as ollama_chat, is_available as ollama_available
        from routers.notifications import notify

        if not ollama_available():
            print(f"[AI Assignment] Ollama not available — skipping for material {material_id}", file=sys.stderr)
            return

        m = db.query(models.Material).filter(models.Material.id == material_id).first()
        course = db.query(models.Course).filter(models.Course.id == course_id).first()
        if not m or not course:
            return

        # Build material content
        text = m.content or ""
        if m.material_type == "file" and m.file_path:
            from pathlib import Path as _Path
            fpath = _Path(m.file_path)
            if fpath.exists():
                try:
                    text = fpath.read_text(encoding="utf-8", errors="ignore")[:4000]
                except Exception:
                    pass
        if not text.strip():
            print(f"[AI Assignment] No text content for material {material_id} — skipping", file=sys.stderr)
            return

        system_prompt = (
            "You are an experienced teacher creating a written assignment based on course material. "
            "Your task is to produce a single, well-structured assignment that tests the student's "
            "understanding of the provided material. "
            "The assignment MUST be appropriate for the course subject provided — all questions and tasks "
            "must relate directly to that subject area and the specific material content. "
            "The assignment must include: a clear title, a concise objective statement, "
            "3–5 specific task prompts or questions the student must answer, "
            "and grading criteria (what earns full marks). "
            "Base everything strictly on the provided material — do not invent topics not covered. "
            "Do NOT include due date placeholders like '[insert date]' or 'due on X' — omit dates entirely. "
            "Do NOT include notes about late submissions or administrative policies. "
            "Output ONLY a valid JSON object with exactly two keys: "
            '{"title": "...", "description": "..."} '
            "where `description` is a plain-text string using \\n for newlines. "
            "Do not include any text, markdown, or explanation outside the JSON object."
        )

        course_context = f"Course: {course.title}"
        if course.subject:
            course_context += f" (Subject: {course.subject})"
        if course.description:
            course_context += f"\nCourse description: {course.description}"

        user_prompt = (
            f"{course_context}\n\n"
            f"Create an assignment based on the following course material titled \"{m.title}\":\n\n"
            f"{text[:4000]}"
        )

        try:
            raw = ollama_chat(
                [{"role": "user", "content": user_prompt}],
                system=system_prompt,
                temperature=0.4,
                max_tokens=1024,
            )
        except Exception as exc:
            print(f"[AI Assignment] Ollama error: {exc}", file=sys.stderr)
            return

        # Parse JSON from response
        import json, re as _re
        title = f"Assignment: {m.title}"
        description = raw.strip()
        match = _re.search(r'\{.*\}', raw, _re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
                title = parsed.get("title", title)
                description = parsed.get("description", description)
            except json.JSONDecodeError:
                pass

        # Clean up description: strip whitespace, remove placeholder date text
        description = description.strip()
        description = _re.sub(r'\[insert date[^\]]*\]', '[date TBD]', description, flags=_re.IGNORECASE)
        # If parsing failed and raw JSON leaked into description, strip it out
        description = _re.sub(r'^\s*\{.*?"description"\s*:\s*"', '', description, flags=_re.DOTALL)
        description = _re.sub(r'"\s*\}\s*$', '', description, flags=_re.DOTALL)
        description = description.strip().strip('"').strip()

        # Create assignment
        assignment = models.Assignment(
            course_id=course_id,
            title=title,
            description=description,
            max_score=100.0,
            unlock_material_id=material_id,
        )
        db.add(assignment)
        db.flush()

        # Notify only the student who completed the material
        notify(
            db, student_id, "assignment",
            f"📋 New assignment: {title}",
            f"{course.title} — generated from \"{m.title}\"",
            link=f"assignment:{assignment.id}",
        )

        db.commit()
        print(f"[AI Assignment] Created assignment '{title}' for course {course_id}", file=sys.stderr)
    except Exception as exc:
        print(f"[AI Assignment] Unexpected error: {exc}", file=sys.stderr)
    finally:
        db.close()


@router.post("/{course_id}/materials/{material_id}/complete")
def complete_material(
    course_id: int,
    material_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    """Mark a material as completed by the current student (idempotent).
    On first completion, triggers AI assignment generation in the background."""
    m = db.query(models.Material).filter(
        models.Material.id == material_id, models.Material.course_id == course_id
    ).first()
    if not m:
        raise HTTPException(404, "Material not found")
    existing = db.query(models.MaterialCompletion).filter(
        models.MaterialCompletion.material_id == material_id,
        models.MaterialCompletion.student_id == current_user.id,
    ).first()
    if not existing:
        db.add(models.MaterialCompletion(
            material_id=material_id,
            student_id=current_user.id,
        ))
        db.commit()
        # Fire AI assignment generation once (first completion of this material by this student)
        background_tasks.add_task(_ai_generate_assignment_for_material, material_id, course_id, current_user.id)
    return {"ok": True}


@router.delete("/{course_id}/materials/{material_id}/complete/{student_id}")
def unmark_material_complete(
    course_id: int,
    material_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Teacher/admin: remove a student's material completion record."""
    security.require_course_access(course_id, current_user, db)
    rec = db.query(models.MaterialCompletion).filter(
        models.MaterialCompletion.material_id == material_id,
        models.MaterialCompletion.student_id == student_id,
    ).first()
    if not rec:
        raise HTTPException(404, "Completion record not found")
    db.delete(rec)
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
