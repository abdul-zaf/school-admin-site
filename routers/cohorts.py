"""
cohorts.py — Cohort management for student groups.

POST   /api/cohorts/                          Create cohort (admin)
GET    /api/cohorts/                          List cohorts (admin/teacher)
GET    /api/cohorts/{id}                      Cohort detail with members (admin/teacher)
PUT    /api/cohorts/{id}                      Update cohort (admin)
DELETE /api/cohorts/{id}                      Delete cohort (admin)
POST   /api/cohorts/{id}/members              Add student to cohort (admin)
DELETE /api/cohorts/{id}/members/{student_id} Remove student from cohort (admin)
POST   /api/cohorts/{id}/enroll-all/{course_id} Bulk-enroll cohort in course (admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import security

router = APIRouter()


class CohortCreate(BaseModel):
    name: str
    year: int
    description: Optional[str] = None


class CohortUpdate(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None


class MemberAdd(BaseModel):
    student_id: int


@router.post("/")
def create_cohort(
    data: CohortCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    cohort = models.Cohort(
        name=data.name,
        year=data.year,
        description=data.description,
        created_by=current_user.id,
    )
    db.add(cohort)
    db.commit()
    db.refresh(cohort)
    return {"id": cohort.id, "name": cohort.name}


@router.get("/")
def list_cohorts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    cohorts = db.query(models.Cohort).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "year": c.year,
            "description": c.description,
            "member_count": len(c.members),
            "created_at": str(c.created_at),
        }
        for c in cohorts
    ]


@router.get("/{cohort_id}")
def get_cohort(
    cohort_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    cohort = db.query(models.Cohort).filter(models.Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(404, "Cohort not found")
    return {
        "id": cohort.id,
        "name": cohort.name,
        "year": cohort.year,
        "description": cohort.description,
        "members": [
            {
                "id": m.id,
                "student_id": m.student_id,
                "student_name": m.student.name if m.student else None,
                "student_email": m.student.email if m.student else None,
                "added_at": str(m.added_at),
            }
            for m in cohort.members
        ],
        "created_at": str(cohort.created_at),
    }


@router.put("/{cohort_id}")
def update_cohort(
    cohort_id: int,
    data: CohortUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    cohort = db.query(models.Cohort).filter(models.Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(404, "Cohort not found")
    if data.name is not None:
        cohort.name = data.name
    if data.year is not None:
        cohort.year = data.year
    if data.description is not None:
        cohort.description = data.description
    db.commit()
    return {"ok": True}


@router.delete("/{cohort_id}")
def delete_cohort(
    cohort_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    cohort = db.query(models.Cohort).filter(models.Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(404, "Cohort not found")
    db.delete(cohort)
    db.commit()
    return {"ok": True}


@router.post("/{cohort_id}/members")
def add_member(
    cohort_id: int,
    data: MemberAdd,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    cohort = db.query(models.Cohort).filter(models.Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(404, "Cohort not found")
    student = db.query(models.User).filter(models.User.id == data.student_id).first()
    if not student or student.role != "student":
        raise HTTPException(400, "User not found or not a student")
    existing = db.query(models.CohortMember).filter(
        models.CohortMember.cohort_id == cohort_id,
        models.CohortMember.student_id == data.student_id,
    ).first()
    if existing:
        raise HTTPException(400, "Student already in cohort")
    m = models.CohortMember(cohort_id=cohort_id, student_id=data.student_id)
    db.add(m)
    db.commit()
    db.refresh(m)
    return {"id": m.id, "student_id": m.student_id}


@router.delete("/{cohort_id}/members/{student_id}")
def remove_member(
    cohort_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    m = db.query(models.CohortMember).filter(
        models.CohortMember.cohort_id == cohort_id,
        models.CohortMember.student_id == student_id,
    ).first()
    if not m:
        raise HTTPException(404, "Member not found in cohort")
    db.delete(m)
    db.commit()
    return {"ok": True}


@router.post("/{cohort_id}/enroll-all/{course_id}")
def bulk_enroll(
    cohort_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    cohort = db.query(models.Cohort).filter(models.Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(404, "Cohort not found")
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    enrolled = 0
    skipped = 0
    for member in cohort.members:
        already = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == course_id,
            models.Enrollment.student_id == member.student_id,
        ).first()
        if already:
            skipped += 1
            continue
        # Check enrollment cap
        if course.enrollment_cap is not None:
            current_count = db.query(models.Enrollment).filter(
                models.Enrollment.course_id == course_id
            ).count()
            if current_count >= course.enrollment_cap:
                # Put remaining on waitlist
                on_waitlist = db.query(models.EnrollmentWaitlist).filter(
                    models.EnrollmentWaitlist.course_id == course_id,
                    models.EnrollmentWaitlist.student_id == member.student_id,
                ).first()
                if not on_waitlist:
                    db.add(models.EnrollmentWaitlist(
                        course_id=course_id,
                        student_id=member.student_id,
                    ))
                skipped += 1
                continue
        db.add(models.Enrollment(student_id=member.student_id, course_id=course_id))
        enrolled += 1
    db.commit()
    return {"enrolled": enrolled, "skipped": skipped}
