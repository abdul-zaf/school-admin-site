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

    # Send email notifications to enrolled students (non-blocking, only for published announcements)
    now = datetime.utcnow()
    if data.course_id and (not data.publish_at or data.publish_at <= now):
        enrollments = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == data.course_id
        ).all()
        course = db.query(models.Course).filter(models.Course.id == data.course_id).first()
        course_title = course.title if course else "Unknown course"
        for enr in enrollments:
            student = db.query(models.User).filter(models.User.id == enr.student_id).first()
            if student and getattr(student, "email_notifications", True):
                background_tasks.add_task(
                    notify_new_announcement,
                    student.email,
                    student.name,
                    course_title,
                    data.title,
                )

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
