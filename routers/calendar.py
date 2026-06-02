"""
calendar.py — Academic calendar events.

POST   /api/calendar/      Create event (admin)
GET    /api/calendar/      List events, optional ?year=&month= filter
PUT    /api/calendar/{id}  Update event (admin)
DELETE /api/calendar/{id}  Delete event (admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import get_db
import models
import security

router = APIRouter()

VALID_TYPES = {"holiday", "exam_week", "term_start", "term_end", "other"}


class CalendarEventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str = "other"
    start_date: date
    end_date: date


class CalendarEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


@router.post("/")
def create_event(
    data: CalendarEventCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    if data.event_type not in VALID_TYPES:
        raise HTTPException(400, f"event_type must be one of: {VALID_TYPES}")
    if data.end_date < data.start_date:
        raise HTTPException(400, "end_date must be >= start_date")
    ev = models.AcademicCalendarEvent(
        title=data.title,
        description=data.description,
        event_type=data.event_type,
        start_date=data.start_date,
        end_date=data.end_date,
        created_by=current_user.id,
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return {"id": ev.id, "title": ev.title}


@router.get("/")
def list_events(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    q = db.query(models.AcademicCalendarEvent)
    if year:
        from sqlalchemy import extract
        q = q.filter(extract("year", models.AcademicCalendarEvent.start_date) == year)
    if month:
        from sqlalchemy import extract
        q = q.filter(extract("month", models.AcademicCalendarEvent.start_date) == month)
    events = q.order_by(models.AcademicCalendarEvent.start_date).all()
    return [
        {
            "id": ev.id,
            "title": ev.title,
            "description": ev.description,
            "event_type": ev.event_type,
            "start_date": str(ev.start_date),
            "end_date": str(ev.end_date),
            "created_by": ev.created_by,
            "created_at": str(ev.created_at),
        }
        for ev in events
    ]


@router.put("/{event_id}")
def update_event(
    event_id: int,
    data: CalendarEventUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    ev = db.query(models.AcademicCalendarEvent).filter(
        models.AcademicCalendarEvent.id == event_id
    ).first()
    if not ev:
        raise HTTPException(404, "Event not found")
    if data.title is not None:
        ev.title = data.title
    if data.description is not None:
        ev.description = data.description
    if data.event_type is not None:
        if data.event_type not in VALID_TYPES:
            raise HTTPException(400, f"event_type must be one of: {VALID_TYPES}")
        ev.event_type = data.event_type
    if data.start_date is not None:
        ev.start_date = data.start_date
    if data.end_date is not None:
        ev.end_date = data.end_date
    db.commit()
    return {"ok": True}


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    ev = db.query(models.AcademicCalendarEvent).filter(
        models.AcademicCalendarEvent.id == event_id
    ).first()
    if not ev:
        raise HTTPException(404, "Event not found")
    db.delete(ev)
    db.commit()
    return {"ok": True}
