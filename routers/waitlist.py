"""
waitlist.py — Enrollment waitlist management.

POST   /api/waitlist/{course_id}   Join waitlist (student)
DELETE /api/waitlist/{course_id}   Leave waitlist (student)
GET    /api/waitlist/{course_id}   View waitlist (teacher/admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import security

router = APIRouter()


@router.post("/{course_id}")
def join_waitlist(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    already_enrolled = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course_id,
        models.Enrollment.student_id == current_user.id,
    ).first()
    if already_enrolled:
        raise HTTPException(400, "Already enrolled in this course")
    already_waiting = db.query(models.EnrollmentWaitlist).filter(
        models.EnrollmentWaitlist.course_id == course_id,
        models.EnrollmentWaitlist.student_id == current_user.id,
    ).first()
    if already_waiting:
        raise HTTPException(400, "Already on the waitlist")
    w = models.EnrollmentWaitlist(course_id=course_id, student_id=current_user.id)
    db.add(w)
    db.commit()
    db.refresh(w)
    return {"ok": True, "joined_at": str(w.joined_at)}


@router.delete("/{course_id}")
def leave_waitlist(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    w = db.query(models.EnrollmentWaitlist).filter(
        models.EnrollmentWaitlist.course_id == course_id,
        models.EnrollmentWaitlist.student_id == current_user.id,
    ).first()
    if not w:
        raise HTTPException(404, "Not on the waitlist for this course")
    db.delete(w)
    db.commit()
    return {"ok": True}


@router.get("/{course_id}")
def get_waitlist(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    waitlist = (
        db.query(models.EnrollmentWaitlist)
        .filter(models.EnrollmentWaitlist.course_id == course_id)
        .order_by(models.EnrollmentWaitlist.joined_at)
        .all()
    )
    return [
        {
            "id": w.id,
            "student_id": w.student_id,
            "student_name": w.student.name if w.student else None,
            "student_email": w.student.email if w.student else None,
            "joined_at": str(w.joined_at),
        }
        for w in waitlist
    ]
