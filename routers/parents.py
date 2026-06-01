"""
parents.py — Parent-student account links.

GET    /api/parents/my-children            Parent views linked children
POST   /api/parents/link                   Link parent to a student
DELETE /api/parents/link/{student_id}      Remove the link
GET    /api/parents/child/{id}/summary     Grade + attendance summary
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import security

router = APIRouter()


class LinkCreate(BaseModel):
    student_id: int
    relation: str = "parent"
    # parent_id only honoured when caller is admin; ignored for parent role
    parent_id: Optional[int] = None


@router.get("/my-students")
def my_students(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("parent")),
):
    links = db.query(models.ParentLink).filter(
        models.ParentLink.parent_id == current_user.id
    ).all()
    result = []
    for link in links:
        student = link.student
        enrollments = db.query(models.Enrollment).filter(
            models.Enrollment.student_id == student.id
        ).all()
        result.append({
            "link_id": link.id,
            "student_id": student.id,
            "student_name": student.name,
            "student_email": student.email,
            "relationship": link.relation,
            "enrolled_courses": len(enrollments),
        })
    return result


@router.get("/student/{student_id}")
def student_overview(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("parent")),
):
    # Verify this parent is linked to this student
    link = db.query(models.ParentLink).filter(
        models.ParentLink.parent_id == current_user.id,
        models.ParentLink.student_id == student_id,
    ).first()
    if not link:
        raise HTTPException(403, "Not linked to this student")

    student = db.query(models.User).filter(models.User.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id
    ).all()

    courses_info = []
    for enr in enrollments:
        course = enr.course
        assignments = db.query(models.Assignment).filter(
            models.Assignment.course_id == course.id
        ).all()
        subs = db.query(models.Submission).filter(
            models.Submission.student_id == student_id,
            models.Submission.assignment_id.in_([a.id for a in assignments]),
        ).all()
        graded = [s for s in subs if s.score is not None]
        avg_score = sum(s.score for s in graded) / len(graded) if graded else None

        courses_info.append({
            "course_id": course.id,
            "course_title": course.title,
            "teacher_name": course.teacher.name if course.teacher else "?",
            "assignment_count": len(assignments),
            "submitted_count": len(subs),
            "graded_count": len(graded),
            "avg_score": round(avg_score, 2) if avg_score is not None else None,
        })

    # Attendance summary
    attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id
    ).all()
    att_summary = {
        "present": sum(1 for a in attendance if a.status == "present"),
        "absent": sum(1 for a in attendance if a.status == "absent"),
        "late": sum(1 for a in attendance if a.status == "late"),
    }

    return {
        "student_id": student.id,
        "student_name": student.name,
        "student_email": student.email,
        "courses": courses_info,
        "attendance": att_summary,
    }


@router.post("/link")
def create_link(
    data: LinkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "parent")),
):
    # Parents link themselves; admins can specify any parent_id
    if current_user.role == "parent":
        parent_id = current_user.id
    else:
        if not data.parent_id:
            raise HTTPException(400, "Admin must supply parent_id")
        parent_id = data.parent_id

    parent = db.query(models.User).filter(models.User.id == parent_id).first()
    if not parent or parent.role != "parent":
        raise HTTPException(400, "Target user must have role 'parent'")

    student = db.query(models.User).filter(models.User.id == data.student_id).first()
    if not student or student.role != "student":
        raise HTTPException(400, "Linked user must be a student")

    if db.query(models.ParentLink).filter(
        models.ParentLink.parent_id == parent_id,
        models.ParentLink.student_id == data.student_id,
    ).first():
        raise HTTPException(400, "Link already exists")

    link = models.ParentLink(parent_id=parent_id, student_id=data.student_id,
                              relation=data.relation)
    db.add(link)
    db.commit()
    db.refresh(link)
    return {"id": link.id, "ok": True}


@router.delete("/link/{link_id}")
def delete_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "parent")),
):
    link = db.query(models.ParentLink).filter(models.ParentLink.id == link_id).first()
    if not link:
        raise HTTPException(404, "Link not found")
    if current_user.role == "parent" and link.parent_id != current_user.id:
        raise HTTPException(403, "You can only remove your own links")
    db.delete(link)
    db.commit()
    return {"ok": True}
