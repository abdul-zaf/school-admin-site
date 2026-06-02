"""
conferences.py — Parent-Teacher Conference scheduling.

POST   /api/conferences/slots                  Create slot (teacher)
GET    /api/conferences/slots                  List available slots
DELETE /api/conferences/slots/{id}             Delete own unbooked slot (teacher)
POST   /api/conferences/book/{slot_id}         Book a slot (parent)
GET    /api/conferences/my-bookings            See own bookings (parent)
GET    /api/conferences/teacher-bookings       See bookings for teacher's slots (teacher)
DELETE /api/conferences/bookings/{id}          Cancel booking (parent/teacher)
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


class SlotCreate(BaseModel):
    date: date
    start_time: str
    end_time: str
    course_id: Optional[int] = None


class BookingCreate(BaseModel):
    student_id: int
    notes: Optional[str] = None


@router.post("/slots")
def create_slot(
    data: SlotCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("teacher", "admin")),
):
    slot = models.ConferenceSlot(
        teacher_id=current_user.id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        course_id=data.course_id,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return {"id": slot.id, "date": str(slot.date), "start_time": slot.start_time, "end_time": slot.end_time}


@router.get("/slots")
def list_slots(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    q = db.query(models.ConferenceSlot)
    if current_user.role == "teacher":
        q = q.filter(models.ConferenceSlot.teacher_id == current_user.id)
    elif current_user.role == "parent":
        # Parents see all unbooked slots
        q = q.filter(models.ConferenceSlot.is_booked == False)
    slots = q.order_by(models.ConferenceSlot.date, models.ConferenceSlot.start_time).all()
    return [
        {
            "id": s.id,
            "teacher_id": s.teacher_id,
            "teacher_name": s.teacher.name if s.teacher else None,
            "date": str(s.date),
            "start_time": s.start_time,
            "end_time": s.end_time,
            "is_booked": s.is_booked,
            "course_id": s.course_id,
        }
        for s in slots
    ]


@router.delete("/slots/{slot_id}")
def delete_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("teacher", "admin")),
):
    slot = db.query(models.ConferenceSlot).filter(models.ConferenceSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(404, "Slot not found")
    if current_user.role == "teacher" and slot.teacher_id != current_user.id:
        raise HTTPException(403, "Not your slot")
    if slot.is_booked:
        raise HTTPException(400, "Cannot delete a booked slot")
    db.delete(slot)
    db.commit()
    return {"ok": True}


@router.post("/book/{slot_id}")
def book_slot(
    slot_id: int,
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("parent")),
):
    slot = db.query(models.ConferenceSlot).filter(models.ConferenceSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(404, "Slot not found")
    if slot.is_booked:
        raise HTTPException(400, "Slot is already booked")
    # Verify the student is linked to this parent
    link = db.query(models.ParentLink).filter(
        models.ParentLink.parent_id == current_user.id,
        models.ParentLink.student_id == data.student_id,
    ).first()
    if not link:
        raise HTTPException(403, "Student is not linked to your account")
    slot.is_booked = True
    booking = models.ConferenceBooking(
        slot_id=slot_id,
        parent_id=current_user.id,
        student_id=data.student_id,
        notes=data.notes,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return {"id": booking.id, "slot_id": slot_id, "booked_at": str(booking.booked_at)}


@router.get("/my-bookings")
def my_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("parent")),
):
    bookings = db.query(models.ConferenceBooking).filter(
        models.ConferenceBooking.parent_id == current_user.id
    ).all()
    return [
        {
            "id": b.id,
            "slot_id": b.slot_id,
            "slot_date": str(b.slot.date) if b.slot else None,
            "start_time": b.slot.start_time if b.slot else None,
            "end_time": b.slot.end_time if b.slot else None,
            "teacher_name": b.slot.teacher.name if b.slot and b.slot.teacher else None,
            "student_id": b.student_id,
            "student_name": b.student.name if b.student else None,
            "notes": b.notes,
            "booked_at": str(b.booked_at),
        }
        for b in bookings
    ]


@router.get("/teacher-bookings")
def teacher_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("teacher", "admin")),
):
    slots = db.query(models.ConferenceSlot).filter(
        models.ConferenceSlot.teacher_id == current_user.id,
        models.ConferenceSlot.is_booked == True,
    ).all()
    result = []
    for slot in slots:
        for b in slot.bookings:
            result.append({
                "booking_id": b.id,
                "slot_id": slot.id,
                "date": str(slot.date),
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "parent_id": b.parent_id,
                "parent_name": b.parent.name if b.parent else None,
                "student_id": b.student_id,
                "student_name": b.student.name if b.student else None,
                "notes": b.notes,
            })
    return result


@router.delete("/bookings/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    booking = db.query(models.ConferenceBooking).filter(
        models.ConferenceBooking.id == booking_id
    ).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    # Only the parent who booked or the teacher of the slot can cancel
    if current_user.role == "parent" and booking.parent_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    if current_user.role == "teacher" and booking.slot.teacher_id != current_user.id:
        raise HTTPException(403, "Not your slot")
    if current_user.role == "student":
        raise HTTPException(403, "Students cannot cancel bookings")
    # Mark slot as available again
    booking.slot.is_booked = False
    db.delete(booking)
    db.commit()
    return {"ok": True}
