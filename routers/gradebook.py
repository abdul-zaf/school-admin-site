"""
gradebook.py — Weighted grade calculation, GPA, and letter grades.

GET    /api/gradebook/my              Student grades across all courses
GET    /api/gradebook/course/{id}     Full gradebook grid (teacher/admin)
POST   /api/gradebook/categories      Create a weighted grade category
PUT    /api/gradebook/categories/{id} Update weight / drop-lowest setting
DELETE /api/gradebook/categories/{id} Remove a grade category
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import security

router = APIRouter()


class CategoryCreate(BaseModel):
    name: str
    weight: float = 100.0
    drop_lowest: int = 0


def score_to_letter(score: float) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"


def letter_to_gpa(letter: str) -> float:
    return {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}.get(letter, 0.0)


def compute_weighted_grade(student_id: int, assignments: list, submissions_map: dict,
                            categories: list) -> dict:
    """
    Compute weighted grade for a student across assignments.
    submissions_map: {assignment_id: submission}
    categories: list of GradeCategory objects
    Returns {weighted_pct, letter, gpa}
    """
    # Group assignments by category
    cat_map = {c.id: c for c in categories}
    # uncategorized goes into a default bucket
    cat_assignments: dict[Optional[int], list] = {}
    for a in assignments:
        if a.is_extra_credit:
            continue
        cid = a.grade_category_id
        cat_assignments.setdefault(cid, []).append(a)

    total_weight = 0.0
    weighted_sum = 0.0

    for cid, asgns in cat_assignments.items():
        cat = cat_map.get(cid)
        weight = cat.weight if cat else 100.0
        drop_n = cat.drop_lowest if cat else 0

        # Collect scores for this category
        scores = []
        for a in asgns:
            sub = submissions_map.get(a.id)
            if sub and sub.score is not None and a.max_score and a.max_score > 0:
                pct = (sub.score / a.max_score) * 100.0
                scores.append(pct)

        if not scores:
            continue

        # Drop lowest N
        if drop_n > 0 and len(scores) > drop_n:
            scores = sorted(scores)[drop_n:]

        avg = sum(scores) / len(scores)
        weighted_sum += avg * weight
        total_weight += weight

    # Extra credit
    extra_points = 0.0
    for a in assignments:
        if not a.is_extra_credit:
            continue
        sub = submissions_map.get(a.id)
        if sub and sub.score is not None:
            extra_points += sub.score

    if total_weight == 0:
        weighted_pct = 0.0
    else:
        weighted_pct = weighted_sum / total_weight

    # Add extra credit as percentage points (simple addition)
    if total_weight > 0:
        # Convert extra_points to percentage relative to total max
        total_max = sum(a.max_score for a in assignments if not a.is_extra_credit and a.max_score)
        if total_max > 0:
            weighted_pct += (extra_points / total_max) * 100.0

    letter = score_to_letter(weighted_pct)
    return {
        "weighted_pct": round(weighted_pct, 2),
        "letter": letter,
        "gpa": letter_to_gpa(letter),
    }


@router.get("/course/{course_id}")
def course_gradebook(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")

    assignments = db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()
    categories = db.query(models.GradeCategory).filter(models.GradeCategory.course_id == course_id).all()
    enrollments = db.query(models.Enrollment).filter(models.Enrollment.course_id == course_id).all()

    result = []
    for enr in enrollments:
        student = enr.student
        subs = db.query(models.Submission).filter(
            models.Submission.student_id == student.id,
            models.Submission.assignment_id.in_([a.id for a in assignments]),
        ).all()
        sub_map = {s.assignment_id: s for s in subs}

        scores = {}
        for a in assignments:
            sub = sub_map.get(a.id)
            scores[a.id] = {
                "submission_id": sub.id if sub else None,
                "score": sub.score if sub else None,
                "max_score": a.max_score,
                "submitted": sub is not None,
                "graded": sub and sub.score is not None,
            }

        grade_info = compute_weighted_grade(student.id, assignments, sub_map, categories)
        result.append({
            "student_id": student.id,
            "student_name": student.name,
            "student_email": student.email,
            "scores": scores,
            **grade_info,
        })

    return {
        "course_id": course_id,
        "course_title": course.title,
        "assignments": [
            {"id": a.id, "title": a.title, "max_score": a.max_score,
             "is_extra_credit": a.is_extra_credit, "category_id": a.grade_category_id}
            for a in assignments
        ],
        "students": result,
    }


@router.get("/course/{course_id}/categories")
def list_categories(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    cats = db.query(models.GradeCategory).filter(models.GradeCategory.course_id == course_id).all()
    return [{"id": c.id, "name": c.name, "weight": c.weight, "drop_lowest": c.drop_lowest} for c in cats]


@router.post("/course/{course_id}/categories")
def create_category(
    course_id: int,
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    cat = models.GradeCategory(
        course_id=course_id,
        name=data.name,
        weight=data.weight,
        drop_lowest=data.drop_lowest,
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return {"id": cat.id, "name": cat.name}


@router.put("/categories/{cat_id}")
def update_category(
    cat_id: int,
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    cat = db.query(models.GradeCategory).filter(models.GradeCategory.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "Category not found")
    security.require_course_access(cat.course_id, current_user, db)
    cat.name = data.name
    cat.weight = data.weight
    cat.drop_lowest = data.drop_lowest
    db.commit()
    return {"ok": True}


@router.delete("/categories/{cat_id}")
def delete_category(
    cat_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    cat = db.query(models.GradeCategory).filter(models.GradeCategory.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "Category not found")
    security.require_course_access(cat.course_id, current_user, db)
    db.delete(cat)
    db.commit()
    return {"ok": True}


@router.get("/my")
def my_gradebook(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == current_user.id
    ).all()

    courses_data = []
    total_gpa = 0.0
    count = 0

    for enr in enrollments:
        course = enr.course
        assignments = db.query(models.Assignment).filter(
            models.Assignment.course_id == course.id
        ).all()
        categories = db.query(models.GradeCategory).filter(
            models.GradeCategory.course_id == course.id
        ).all()
        subs = db.query(models.Submission).filter(
            models.Submission.student_id == current_user.id,
            models.Submission.assignment_id.in_([a.id for a in assignments]),
        ).all()
        sub_map = {s.assignment_id: s for s in subs}

        grade_info = compute_weighted_grade(current_user.id, assignments, sub_map, categories)
        scores = {}
        for a in assignments:
            sub = sub_map.get(a.id)
            scores[a.id] = {
                "title": a.title,
                "score": sub.score if sub else None,
                "max_score": a.max_score,
                "submitted": sub is not None,
            }

        courses_data.append({
            "course_id": course.id,
            "course_title": course.title,
            "scores": scores,
            **grade_info,
        })

        if grade_info["weighted_pct"] > 0 or assignments:
            total_gpa += grade_info["gpa"]
            count += 1

    cumulative_gpa = round(total_gpa / count, 2) if count else 0.0
    return {"courses": courses_data, "cumulative_gpa": cumulative_gpa}


@router.get("/course/{course_id}/student/{student_id}")
def student_grade_detail(
    course_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    # Students can only see their own, teachers/admins can see any
    if current_user.role == "student" and current_user.id != student_id:
        raise HTTPException(403, "Access denied")
    if current_user.role in ("admin", "teacher"):
        security.require_course_access(course_id, current_user, db)

    assignments = db.query(models.Assignment).filter(
        models.Assignment.course_id == course_id
    ).all()
    categories = db.query(models.GradeCategory).filter(
        models.GradeCategory.course_id == course_id
    ).all()
    subs = db.query(models.Submission).filter(
        models.Submission.student_id == student_id,
        models.Submission.assignment_id.in_([a.id for a in assignments]),
    ).all()
    sub_map = {s.assignment_id: s for s in subs}
    grade_info = compute_weighted_grade(student_id, assignments, sub_map, categories)

    details = []
    for a in assignments:
        sub = sub_map.get(a.id)
        details.append({
            "assignment_id": a.id,
            "title": a.title,
            "max_score": a.max_score,
            "is_extra_credit": a.is_extra_credit,
            "score": sub.score if sub else None,
            "feedback": sub.feedback if sub else None,
            "submitted_at": str(sub.submitted_at) if sub else None,
        })

    return {
        "course_id": course_id,
        "student_id": student_id,
        "assignments": details,
        **grade_info,
    }
