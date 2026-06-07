"""
modules.py — Ordered course modules with completion tracking.

GET    /api/modules/course/{id}         List modules for a course
POST   /api/modules/course/{id}         Create a module (teacher/admin)
PUT    /api/modules/{id}                Rename / reorder a module
DELETE /api/modules/{id}                Delete a module
POST   /api/modules/{id}/items          Add an item to a module
DELETE /api/modules/items/{id}          Remove a module item
POST   /api/modules/items/{id}/complete Student marks an item complete
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


class ModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    order_num: int = 0
    is_published: bool = True


_VALID_ITEM_TYPES = {"assignment", "quiz", "material", "session", "page"}

class ModuleItemCreate(BaseModel):
    item_type: str  # assignment | quiz | material | session | page
    item_id: Optional[int] = None
    title: str
    order_num: int = 0
    is_required: bool = True

    @field_validator("item_type")
    @classmethod
    def validate_item_type(cls, v: str) -> str:
        if v not in _VALID_ITEM_TYPES:
            raise ValueError(f"item_type must be one of: {', '.join(sorted(_VALID_ITEM_TYPES))}")
        return v


@router.get("/course/{course_id}")
def list_modules(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    modules = (
        db.query(models.CourseModule)
        .filter(models.CourseModule.course_id == course_id)
        .order_by(models.CourseModule.order_num)
        .all()
    )

    # Get completions for current student
    completed_item_ids = set()
    if current_user.role == "student":
        completions = db.query(models.ModuleCompletion).filter(
            models.ModuleCompletion.student_id == current_user.id
        ).all()
        completed_item_ids = {c.module_item_id for c in completions}

    result = []
    for m in modules:
        items = []
        for item in m.items:
            items.append({
                "id": item.id,
                "item_type": item.item_type,
                "item_id": item.item_id,
                "title": item.title,
                "order_num": item.order_num,
                "is_required": item.is_required,
                "completed": item.id in completed_item_ids,
            })
        required_items = [i for i in items if i["is_required"]]
        completed_required = sum(1 for i in required_items if i["completed"])
        progress = (
            int(completed_required / len(required_items) * 100)
            if required_items else 100
        )
        result.append({
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "order_num": m.order_num,
            "is_published": m.is_published,
            "items": items,
            "progress": progress,
        })
    return result


@router.post("/course/{course_id}")
def create_module(
    course_id: int,
    data: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    module = models.CourseModule(
        course_id=course_id,
        title=data.title,
        description=data.description,
        order_num=data.order_num,
        is_published=data.is_published,
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    return {"id": module.id, "title": module.title}


@router.put("/{module_id}")
def update_module(
    module_id: int,
    data: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    module = db.query(models.CourseModule).filter(models.CourseModule.id == module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    security.require_course_access(module.course_id, current_user, db)
    module.title = data.title
    module.description = data.description
    module.order_num = data.order_num
    module.is_published = data.is_published
    db.commit()
    return {"ok": True}


@router.delete("/{module_id}")
def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    module = db.query(models.CourseModule).filter(models.CourseModule.id == module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    security.require_course_access(module.course_id, current_user, db)
    db.delete(module)
    db.commit()
    return {"ok": True}


@router.post("/{module_id}/items")
def add_module_item(
    module_id: int,
    data: ModuleItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    module = db.query(models.CourseModule).filter(models.CourseModule.id == module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    security.require_course_access(module.course_id, current_user, db)
    item = models.ModuleItem(
        module_id=module_id,
        item_type=data.item_type,
        item_id=data.item_id,
        title=data.title,
        order_num=data.order_num,
        is_required=data.is_required,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "title": item.title}


@router.delete("/items/{item_id}")
def delete_module_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    item = db.query(models.ModuleItem).filter(models.ModuleItem.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")
    module = db.query(models.CourseModule).filter(models.CourseModule.id == item.module_id).first()
    security.require_course_access(module.course_id, current_user, db)
    db.delete(item)
    db.commit()
    return {"ok": True}


@router.post("/items/{item_id}/complete")
def complete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    item = db.query(models.ModuleItem).filter(models.ModuleItem.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")
    existing = db.query(models.ModuleCompletion).filter(
        models.ModuleCompletion.module_item_id == item_id,
        models.ModuleCompletion.student_id == current_user.id,
    ).first()
    if existing:
        return {"ok": True, "already_completed": True}
    completion = models.ModuleCompletion(
        module_item_id=item_id,
        student_id=current_user.id,
    )
    db.add(completion)
    db.commit()
    try:
        from routers.notifications import notify
        module = db.query(models.CourseModule).filter(models.CourseModule.id == item.module_id).first()
        if module:
            course = db.query(models.Course).filter(models.Course.id == module.course_id).first()
            if course:
                notify(db, course.teacher_id, "completion",
                       f"{current_user.name} completed a module item",
                       f'"{item.title}" in {course.title}',
                       f"courses?id={course.id}")
                db.commit()
    except Exception:
        pass
    return {"ok": True}
