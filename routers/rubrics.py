"""
rubrics.py — Criterion-based grading rubrics attached to assignments.

GET    /api/rubrics/course/{id}           List rubrics for a course
POST   /api/rubrics/course/{id}           Create a rubric
GET    /api/rubrics/{id}                  Rubric detail
PUT    /api/rubrics/{id}                  Update rubric
DELETE /api/rubrics/{id}                  Delete rubric
POST   /api/rubrics/{id}/grade/{sub_id}   Apply rubric to a submission
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import security

router = APIRouter()


class RubricLevelIn(BaseModel):
    label: str
    description: Optional[str] = None
    points: float = 0.0


class RubricCriterionIn(BaseModel):
    title: str
    description: Optional[str] = None
    max_points: float = 10.0
    order_num: int = 0
    levels: List[RubricLevelIn] = []


class RubricCreate(BaseModel):
    name: str
    description: Optional[str] = None
    course_id: Optional[int] = None
    criteria: List[RubricCriterionIn] = []


class RubricGradeItem(BaseModel):
    criterion_id: int
    points_awarded: float
    comment: Optional[str] = None


@router.get("/course/{course_id}")
def list_rubrics(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    rubrics = db.query(models.Rubric).filter(models.Rubric.course_id == course_id).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "course_id": r.course_id,
            "criterion_count": len(r.criteria),
        }
        for r in rubrics
    ]


@router.post("/")
def create_rubric(
    data: RubricCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    if data.course_id:
        security.require_course_access(data.course_id, current_user, db)

    rubric = models.Rubric(
        course_id=data.course_id,
        name=data.name,
        description=data.description,
        creator_id=current_user.id,
    )
    db.add(rubric)
    db.flush()

    for i, c_data in enumerate(data.criteria):
        criterion = models.RubricCriterion(
            rubric_id=rubric.id,
            title=c_data.title,
            description=c_data.description,
            max_points=c_data.max_points,
            order_num=c_data.order_num if c_data.order_num else i,
        )
        db.add(criterion)
        db.flush()
        for lv in c_data.levels:
            level = models.RubricLevel(
                criterion_id=criterion.id,
                label=lv.label,
                description=lv.description,
                points=lv.points,
            )
            db.add(level)

    db.commit()
    db.refresh(rubric)
    return {"id": rubric.id, "name": rubric.name}


@router.get("/{rubric_id}")
def get_rubric(
    rubric_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    rubric = db.query(models.Rubric).filter(models.Rubric.id == rubric_id).first()
    if not rubric:
        raise HTTPException(404, "Rubric not found")
    return {
        "id": rubric.id,
        "name": rubric.name,
        "description": rubric.description,
        "course_id": rubric.course_id,
        "criteria": [
            {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "max_points": c.max_points,
                "order_num": c.order_num,
                "levels": [
                    {"id": lv.id, "label": lv.label, "description": lv.description, "points": lv.points}
                    for lv in c.levels
                ],
            }
            for c in rubric.criteria
        ],
    }


@router.delete("/{rubric_id}")
def delete_rubric(
    rubric_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    rubric = db.query(models.Rubric).filter(models.Rubric.id == rubric_id).first()
    if not rubric:
        raise HTTPException(404, "Rubric not found")
    if rubric.course_id:
        security.require_course_access(rubric.course_id, current_user, db)
    db.delete(rubric)
    db.commit()
    return {"ok": True}


@router.post("/{rubric_id}/assign/{assignment_id}")
def assign_rubric(
    rubric_id: int,
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    rubric = db.query(models.Rubric).filter(models.Rubric.id == rubric_id).first()
    if not rubric:
        raise HTTPException(404, "Rubric not found")
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(404, "Assignment not found")
    security.require_course_access(assignment.course_id, current_user, db)
    assignment.rubric_id = rubric_id
    db.commit()
    return {"ok": True}


@router.post("/grade/{submission_id}")
def grade_by_rubric(
    submission_id: int,
    grades: List[RubricGradeItem],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    sub = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(404, "Submission not found")
    security.require_course_access(sub.assignment.course_id, current_user, db)

    # Remove existing rubric grades for this submission
    db.query(models.RubricGrade).filter(models.RubricGrade.submission_id == submission_id).delete()

    total_points = 0.0
    for g in grades:
        criterion = db.query(models.RubricCriterion).filter(
            models.RubricCriterion.id == g.criterion_id
        ).first()
        if not criterion:
            continue
        rg = models.RubricGrade(
            submission_id=submission_id,
            criterion_id=g.criterion_id,
            points_awarded=g.points_awarded,
            comment=g.comment,
        )
        db.add(rg)
        total_points += g.points_awarded

    # Update submission score from rubric total
    from datetime import datetime
    sub.score = total_points
    sub.graded_at = datetime.utcnow()
    db.commit()
    return {"ok": True, "total_points": total_points}
