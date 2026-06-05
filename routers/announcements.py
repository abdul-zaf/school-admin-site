"""
announcements.py — School-wide and per-course announcements.

GET    /api/announcements/           List announcements (filter by course_id)
POST   /api/announcements/           Create announcement (teacher/admin)
DELETE /api/announcements/{id}       Delete announcement (teacher/admin)
"""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models
import security
from services.email import notify_new_announcement
from routers.notifications import notify as push_notif

router = APIRouter()


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    course_id: Optional[int] = None
    publish_at: Optional[datetime] = None   # future = draft until that time


@router.get("/")
def list_announcements(
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    q = db.query(models.Announcement)
    if course_id:
        q = q.filter(models.Announcement.course_id == course_id)
    else:
        q = q.filter(models.Announcement.course_id == None)

    now = datetime.utcnow()
    is_privileged = current_user.role in ("teacher", "admin")
    announcements = q.order_by(models.Announcement.created_at.desc()).all()

    result = []
    for a in announcements:
        # Hide draft announcements from students
        if not is_privileged and a.publish_at and a.publish_at > now:
            continue
        result.append({
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "author_name": a.author.name if a.author else None,
            "course_id": a.course_id,
            "created_at": str(a.created_at),
            "publish_at": str(a.publish_at) if a.publish_at else None,
            "is_draft": bool(a.publish_at and a.publish_at > now),
        })
    return result


@router.post("/")
def create_announcement(
    data: AnnouncementCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    a = models.Announcement(
        title=data.title,
        content=data.content,
        author_id=current_user.id,
        course_id=data.course_id,
        publish_at=data.publish_at,
    )
    db.add(a)
    db.commit()
    db.refresh(a)

    now = datetime.utcnow()
    is_published = not data.publish_at or data.publish_at <= now

    if is_published:
        notif_body = data.content[:150] + ("…" if len(data.content) > 150 else "")

        if data.course_id:
            # ── Course-specific announcement ──────────────────────────────────
            course = db.query(models.Course).filter(models.Course.id == data.course_id).first()
            course_title = course.title if course else "your course"
            enrollments = db.query(models.Enrollment).filter(
                models.Enrollment.course_id == data.course_id
            ).all()
            student_ids = {enr.student_id for enr in enrollments}

            # Admin posting → also notify the course teacher
            notify_ids = set(student_ids)
            if current_user.role == "admin" and course and course.teacher_id:
                notify_ids.add(course.teacher_id)

            for uid in notify_ids:
                if uid != current_user.id:
                    push_notif(db, uid, "announcement",
                               f"📢 {data.title}", notif_body)

            # Email notifications to enrolled students
            for enr in enrollments:
                student = db.query(models.User).filter(models.User.id == enr.student_id).first()
                if student and getattr(student, "email_notifications", True):
                    background_tasks.add_task(
                        notify_new_announcement,
                        student.email, student.name, course_title, data.title,
                    )
        else:
            # ── School-wide announcement ──────────────────────────────────────
            # Notify all students
            for student in db.query(models.User).filter(models.User.role == "student").all():
                push_notif(db, student.id, "announcement",
                           f"📢 {data.title}", notif_body)

            # If posted by admin, also notify all teachers
            if current_user.role == "admin":
                for teacher in db.query(models.User).filter(models.User.role == "teacher").all():
                    if teacher.id != current_user.id:
                        push_notif(db, teacher.id, "announcement",
                                   f"📢 {data.title}", notif_body)

    db.commit()
    return {"id": a.id, "publish_at": str(a.publish_at) if a.publish_at else None}


@router.delete("/{announcement_id}")
def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    a = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    if not a:
        raise HTTPException(404, "Announcement not found")
    if current_user.role == "teacher" and a.author_id != current_user.id:
        raise HTTPException(403, "Not your announcement")
    db.delete(a)
    db.commit()
    return {"ok": True}
