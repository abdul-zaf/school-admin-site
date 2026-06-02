"""
prerequisites.py - Course prerequisites and sequencing.

POST   /api/prerequisites/                      Add prerequisite (teacher/admin)
GET    /api/prerequisites/course/{course_id}    List prerequisites for a course
DELETE /api/prerequisites/{id}                  Remove prerequisite (teacher/admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import security

router = APIRouter()


class PrerequisiteCreate(BaseModel):
    course_id: int
    prerequisite_course_id: int


def _has_circular(db: Session, course_id: int, prereq_id: int, visited=None) -> bool:
    """Returns True if adding prereq_id as a prerequisite of course_id creates a cycle."""
    if visited is None:
        visited = set()
    if prereq_id == course_id:
        return True
    if prereq_id in visited:
        return False
    visited.add(prereq_id)
    # What are the prerequisites of prereq_id? If course_id is reachable from there, it is circular.
    upstream = db.query(models.CoursePrerequisite).filter(
        models.CoursePrerequisite.course_id == prereq_id
    ).all()
    for up in upstream:
        if _has_circular(db, course_id, up.prerequisite_course_id, visited):
            return True
    return False


@router.post("/")
def add_prerequisite(
    data: PrerequisiteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    if not db.query(models.Course).filter(models.Course.id == data.course_id).first():
        raise HTTPException(404, "Course not found")
    if not db.query(models.Course).filter(models.Course.id == data.prerequisite_course_id).first():
        raise HTTPException(404, "Prerequisite course not found")
    if data.course_id == data.prerequisite_course_id:
        raise HTTPException(400, "A course cannot be its own prerequisite")
    existing = db.query(models.CoursePrerequisite).filter(
        models.CoursePrerequisite.course_id == data.course_id,
        models.CoursePrerequisite.prerequisite_course_id == data.prerequisite_course_id,
    ).first()
    if existing:
        raise HTTPException(400, "Prerequisite already set")
    if _has_circular(db, data.course_id, data.prerequisite_course_id):
        raise HTTPException(400, "Adding this prerequisite would create a circular dependency")
    p = models.CoursePrerequisite(
        course_id=data.course_id,
        prerequisite_course_id=data.prerequisite_course_id,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "course_id": p.course_id, "prerequisite_course_id": p.prerequisite_course_id}


@router.get("/course/{course_id}")
def list_prerequisites(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    prereqs = db.query(models.CoursePrerequisite).filter(
        models.CoursePrerequisite.course_id == course_id
    ).all()
    return [
        {
            "id": p.id,
            "prerequisite_course_id": p.prerequisite_course_id,
            "prerequisite_title": p.prerequisite.title if p.prerequisite else None,
        }
        for p in prereqs
    ]


@router.delete("/{prereq_id}")
def remove_prerequisite(
    prereq_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    p = db.query(models.CoursePrerequisite).filter(models.CoursePrerequisite.id == prereq_id).first()
    if not p:
        raise HTTPException(404, "Prerequisite not found")
    db.delete(p)
    db.commit()
    return {"ok": True}
