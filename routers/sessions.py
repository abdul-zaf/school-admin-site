"""
sessions.py — Virtual and in-person class sessions.

GET    /api/sessions/course/{id}          List sessions for a course
POST   /api/sessions/course/{id}          Schedule a session (own teacher/admin)
DELETE /api/sessions/{id}                 Cancel / delete a session
POST   /api/sessions/{session_id}/meeting Set meeting URL (teacher/admin)
GET    /api/sessions/{session_id}/meeting Get meeting info
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database import get_db
import models
import security

router = APIRouter()


class SessionCreate(BaseModel):
    title: str
    session_type: str       # "virtual" or "physical"
    date: datetime
    duration_minutes: int = 60
    location: Optional[str] = None
    notes: Optional[str] = None


class MeetingSet(BaseModel):
    meeting_url: str
    provider: str = "other"   # zoom | google_meet | teams | other


@router.get("/course/{course_id}")
def list_sessions(
    course_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    sessions = (
        db.query(models.ClassSession)
        .filter(models.ClassSession.course_id == course_id)
        .order_by(models.ClassSession.date)
        .all()
    )
    return [
        {
            "id": s.id,
            "title": s.title,
            "session_type": s.session_type,
            "date": str(s.date),
            "duration_minutes": s.duration_minutes,
            "location": s.location,
            "notes": s.notes,
        }
        for s in sessions
    ]


@router.post("/course/{course_id}")
def create_session(
    course_id: int,
    data: SessionCreate,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    # Verify the caller owns this course (or is admin)
    security.require_course_access(course_id, current_user, db)

    if data.session_type not in ("virtual", "physical"):
        raise HTTPException(400, "session_type must be 'virtual' or 'physical'")

    s = models.ClassSession(
        course_id=course_id,
        title=data.title,
        session_type=data.session_type,
        date=data.date,
        duration_minutes=data.duration_minutes,
        location=data.location,
        notes=data.notes,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id, "title": s.title}


@router.delete("/{session_id}")
def delete_session(
    session_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    s = db.query(models.ClassSession).filter(models.ClassSession.id == session_id).first()
    if not s:
        raise HTTPException(404, "Session not found")
    # Only the course's teacher or an admin may delete sessions
    security.require_course_access(s.course_id, current_user, db)
    db.delete(s)
    db.commit()
    return {"ok": True}


@router.post("/{session_id}/meeting")
def set_meeting(
    session_id: int,
    data: MeetingSet,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    s = db.query(models.ClassSession).filter(models.ClassSession.id == session_id).first()
    if not s:
        raise HTTPException(404, "Session not found")
    security.require_course_access(s.course_id, current_user, db)
    valid_providers = {"zoom", "google_meet", "teams", "other"}
    if data.provider not in valid_providers:
        raise HTTPException(400, f"provider must be one of {valid_providers}")
    # Store as "provider:url" in the location field
    s.location = f"{data.provider}:{data.meeting_url}"
    s.session_type = "virtual"
    db.commit()
    return {"ok": True, "location": s.location}


@router.get("/{session_id}/meeting")
def get_meeting(
    session_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    s = db.query(models.ClassSession).filter(models.ClassSession.id == session_id).first()
    if not s:
        raise HTTPException(404, "Session not found")
    if not s.location:
        return {"meeting_url": None, "provider": None}
    # Parse "provider:url" format
    valid_providers = {"zoom", "google_meet", "teams", "other"}
    parts = s.location.split(":", 1)
    if len(parts) == 2 and parts[0] in valid_providers:
        return {"provider": parts[0], "meeting_url": parts[1]}
    # Legacy location (plain URL or physical address)
    return {"provider": "other", "meeting_url": s.location}
