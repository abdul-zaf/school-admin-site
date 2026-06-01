"""
announcements.py — School-wide and per-course announcements.

GET    /api/announcements/           List announcements (filter by course_id)
POST   /api/announcements/           Create announcement (teacher/admin)
DELETE /api/announcements/{id}       Delete announcement (teacher/admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import security

router = APIRouter()


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    course_id: Optional[int] = None


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
    return [
        {
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "author_name": a.author.name if a.author else None,
            "course_id": a.course_id,
            "created_at": str(a.created_at),
        }
        for a in q.order_by(models.Announcement.created_at.desc()).all()
    ]


@router.post("/")
def create_announcement(
    data: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    a = models.Announcement(
        title=data.title,
        content=data.content,
        author_id=current_user.id,
        course_id=data.course_id,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return {"id": a.id}


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
