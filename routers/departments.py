"""
departments.py — Departments and faculty management.

POST   /api/departments/                         Create department (admin)
GET    /api/departments/                         List departments with member count
GET    /api/departments/{id}                     Department detail with members
PUT    /api/departments/{id}                     Update department (admin)
DELETE /api/departments/{id}                     Delete department (admin)
POST   /api/departments/{id}/members             Add teacher to department (admin)
DELETE /api/departments/{id}/members/{teacher_id} Remove member (admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import security

router = APIRouter()


class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    hod_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    hod_id: Optional[int] = None


class MemberAdd(BaseModel):
    teacher_id: int
    role: str = "member"


@router.post("/")
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    existing = db.query(models.Department).filter(models.Department.name == data.name).first()
    if existing:
        raise HTTPException(400, "Department name already exists")
    dept = models.Department(
        name=data.name,
        description=data.description,
        hod_id=data.hod_id,
    )
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return {"id": dept.id, "name": dept.name}


@router.get("/")
def list_departments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    depts = db.query(models.Department).all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "description": d.description,
            "hod_id": d.hod_id,
            "hod_name": d.hod.name if d.hod else None,
            "member_count": len(d.members),
            "created_at": str(d.created_at),
        }
        for d in depts
    ]


@router.get("/{dept_id}")
def get_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(404, "Department not found")
    return {
        "id": dept.id,
        "name": dept.name,
        "description": dept.description,
        "hod_id": dept.hod_id,
        "hod_name": dept.hod.name if dept.hod else None,
        "members": [
            {
                "id": m.id,
                "teacher_id": m.teacher_id,
                "teacher_name": m.teacher.name if m.teacher else None,
                "role": m.role,
                "joined_at": str(m.joined_at),
            }
            for m in dept.members
        ],
        "created_at": str(dept.created_at),
    }


@router.put("/{dept_id}")
def update_department(
    dept_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(404, "Department not found")
    if data.name is not None:
        dept.name = data.name
    if data.description is not None:
        dept.description = data.description
    if data.hod_id is not None:
        dept.hod_id = data.hod_id
    db.commit()
    return {"ok": True}


@router.delete("/{dept_id}")
def delete_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(404, "Department not found")
    db.delete(dept)
    db.commit()
    return {"ok": True}


@router.post("/{dept_id}/members")
def add_member(
    dept_id: int,
    data: MemberAdd,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(404, "Department not found")
    teacher = db.query(models.User).filter(models.User.id == data.teacher_id).first()
    if not teacher or teacher.role not in ("teacher", "admin"):
        raise HTTPException(400, "User not found or not a teacher")
    existing = db.query(models.DepartmentMember).filter(
        models.DepartmentMember.department_id == dept_id,
        models.DepartmentMember.teacher_id == data.teacher_id,
    ).first()
    if existing:
        raise HTTPException(400, "Teacher already in this department")
    if data.role not in ("member", "hod"):
        raise HTTPException(400, "role must be 'member' or 'hod'")
    m = models.DepartmentMember(
        department_id=dept_id,
        teacher_id=data.teacher_id,
        role=data.role,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return {"id": m.id, "teacher_id": m.teacher_id, "role": m.role}


@router.delete("/{dept_id}/members/{teacher_id}")
def remove_member(
    dept_id: int,
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    m = db.query(models.DepartmentMember).filter(
        models.DepartmentMember.department_id == dept_id,
        models.DepartmentMember.teacher_id == teacher_id,
    ).first()
    if not m:
        raise HTTPException(404, "Member not found in department")
    db.delete(m)
    db.commit()
    return {"ok": True}
