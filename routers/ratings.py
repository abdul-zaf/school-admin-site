"""
ratings.py — Course ratings and reviews.

POST   /api/ratings/course/{course_id}   Submit/update rating (student, must be enrolled)
GET    /api/ratings/course/{course_id}   List ratings with average
DELETE /api/ratings/{id}                 Delete rating (student owner / admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from database import get_db
import models
import security

router = APIRouter()


class RatingCreate(BaseModel):
    rating: int
    review: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v


@router.post("/course/{course_id}")
def submit_rating(
    course_id: int,
    data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    enrolled = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course_id,
        models.Enrollment.student_id == current_user.id,
    ).first()
    if not enrolled:
        raise HTTPException(400, "You must be enrolled to rate this course")
    existing = db.query(models.CourseRating).filter(
        models.CourseRating.course_id == course_id,
        models.CourseRating.student_id == current_user.id,
    ).first()
    if existing:
        existing.rating = data.rating
        existing.review = data.review
        existing.updated_at = datetime.utcnow()
        db.commit()
        return {"id": existing.id, "updated": True}
    r = models.CourseRating(
        course_id=course_id,
        student_id=current_user.id,
        rating=data.rating,
        review=data.review,
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return {"id": r.id, "created": True}


@router.get("/course/{course_id}")
def list_ratings(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    ratings = db.query(models.CourseRating).filter(
        models.CourseRating.course_id == course_id
    ).order_by(models.CourseRating.created_at.desc()).all()
    avg = round(sum(r.rating for r in ratings) / len(ratings), 2) if ratings else None
    return {
        "course_id": course_id,
        "average_rating": avg,
        "total_ratings": len(ratings),
        "ratings": [
            {
                "id": r.id,
                "rating": r.rating,
                "review": r.review,
                "student_name": r.student.name if r.student else None,
                "created_at": str(r.created_at),
                "updated_at": str(r.updated_at),
            }
            for r in ratings
        ],
    }


@router.delete("/{rating_id}")
def delete_rating(
    rating_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    r = db.query(models.CourseRating).filter(models.CourseRating.id == rating_id).first()
    if not r:
        raise HTTPException(404, "Rating not found")
    if current_user.role == "student" and r.student_id != current_user.id:
        raise HTTPException(403, "Not your rating")
    if current_user.role not in ("admin", "student"):
        raise HTTPException(403, "Only students (own rating) or admin can delete ratings")
    db.delete(r)
    db.commit()
    return {"ok": True}
