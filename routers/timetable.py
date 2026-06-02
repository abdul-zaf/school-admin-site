"""
timetable.py — Weekly timetable and schedule builder.

POST /api/timetable/                   Add timetable slot (teacher/admin)
GET  /api/timetable/course/{course_id} Weekly timetable for a course
GET  /api/timetable/my                 Personal timetable across all enrolled courses
PUT  /api/timetable/{id}               Update slot (teacher/admin)
DELETE /api/timetable/{id}             Delete slot (teacher/admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import security

router = APIRouter()

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class SlotCreate(BaseModel):
    course_id: int
    day_of_week: int   # 0=Mon ... 6=Sun
    start_time: str    # HH:MM
    end_time: str      # HH:MM
    room: Optional[str] = None
    recurring: bool = True


class SlotUpdate(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    room: Optional[str] = None
    recurring: Optional[bool] = None


def _slot_dict(s: models.TimetableSlot):
    return {
        "id": s.id,
        "course_id": s.course_id,
        "course_title": s.course.title if s.course else None,
        "day_of_week": s.day_of_week,
        "day_name": DAY_NAMES[s.day_of_week] if 0 <= s.day_of_week <= 6 else "Unknown",
        "start_time": s.start_time,
        "end_time": s.end_time,
        "room": s.room,
        "recurring": s.recurring,
    }


@router.post("/")
def add_slot(
    data: SlotCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    if not (0 <= data.day_of_week <= 6):
        raise HTTPException(400, "day_of_week must be 0-6 (Mon=0, Sun=6)")
    security.require_course_access(data.course_id, current_user, db)
    slot = models.TimetableSlot(
        course_id=data.course_id,
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
        room=data.room,
        recurring=data.recurring,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return _slot_dict(slot)


@router.get("/course/{course_id}")
def course_timetable(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    slots = db.query(models.TimetableSlot).filter(
        models.TimetableSlot.course_id == course_id
    ).order_by(models.TimetableSlot.day_of_week, models.TimetableSlot.start_time).all()
    return [_slot_dict(s) for s in slots]


@router.get("/my")
def my_timetable(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    if current_user.role == "student":
        enrollments = db.query(models.Enrollment).filter(
            models.Enrollment.student_id == current_user.id
        ).all()
        course_ids = [e.course_id for e in enrollments]
    elif current_user.role == "teacher":
        courses = db.query(models.Course).filter(
            models.Course.teacher_id == current_user.id
        ).all()
        course_ids = [c.id for c in courses]
    else:
        # Admin sees everything
        course_ids = [c.id for c in db.query(models.Course).all()]

    if not course_ids:
        return []

    slots = db.query(models.TimetableSlot).filter(
        models.TimetableSlot.course_id.in_(course_ids)
    ).order_by(models.TimetableSlot.day_of_week, models.TimetableSlot.start_time).all()
    return [_slot_dict(s) for s in slots]


@router.put("/{slot_id}")
def update_slot(
    slot_id: int,
    data: SlotUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    slot = db.query(models.TimetableSlot).filter(models.TimetableSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(404, "Slot not found")
    security.require_course_access(slot.course_id, current_user, db)
    for field, val in data.model_dump(exclude_none=True).items():
        setattr(slot, field, val)
    db.commit()
    return _slot_dict(slot)


@router.delete("/{slot_id}")
def delete_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    slot = db.query(models.TimetableSlot).filter(models.TimetableSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(404, "Slot not found")
    security.require_course_access(slot.course_id, current_user, db)
    db.delete(slot)
    db.commit()
    return {"ok": True}
