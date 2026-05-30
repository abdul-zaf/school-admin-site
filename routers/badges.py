from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models
import security
from routers.notifications import notify

router = APIRouter()


class BadgeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    icon: str = "🏅"
    course_id: Optional[int] = None


class AwardNote(BaseModel):
    note: Optional[str] = None


@router.get("/")
def list_badges(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    if current_user.role == "admin":
        badges = db.query(models.Badge).all()
    elif current_user.role == "teacher":
        # Own course badges + global badges
        badges = db.query(models.Badge).filter(
            (models.Badge.created_by == current_user.id) | (models.Badge.course_id == None)
        ).all()
    else:
        badges = db.query(models.Badge).all()

    return [
        {
            "id": b.id,
            "name": b.name,
            "description": b.description,
            "icon": b.icon,
            "course_id": b.course_id,
            "awarded_count": len(b.user_badges),
        }
        for b in badges
    ]


@router.post("/")
def create_badge(
    data: BadgeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    if data.course_id:
        security.require_course_access(data.course_id, current_user, db)
    badge = models.Badge(
        name=data.name,
        description=data.description,
        icon=data.icon,
        course_id=data.course_id,
        created_by=current_user.id,
    )
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return {"id": badge.id, "name": badge.name}


@router.delete("/{badge_id}")
def delete_badge(
    badge_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    badge = db.query(models.Badge).filter(models.Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(404, "Badge not found")
    if current_user.role != "admin" and badge.created_by != current_user.id:
        raise HTTPException(403, "Access denied")
    db.delete(badge)
    db.commit()
    return {"ok": True}


@router.post("/{badge_id}/award/{user_id}")
def award_badge(
    badge_id: int,
    user_id: int,
    data: AwardNote = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    badge = db.query(models.Badge).filter(models.Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(404, "Badge not found")
    recipient = db.query(models.User).filter(models.User.id == user_id).first()
    if not recipient:
        raise HTTPException(404, "User not found")

    # Check not already awarded
    existing = db.query(models.UserBadge).filter(
        models.UserBadge.badge_id == badge_id,
        models.UserBadge.user_id == user_id,
    ).first()
    if existing:
        raise HTTPException(400, "Badge already awarded to this user")

    note = data.note if data else None
    ub = models.UserBadge(
        user_id=user_id,
        badge_id=badge_id,
        awarded_by=current_user.id,
        note=note,
    )
    db.add(ub)
    notify(db, user_id, "badge_awarded", f"You earned the badge: {badge.icon} {badge.name}",
           note or "", "/badges/my")
    db.commit()
    return {"ok": True}


@router.get("/my")
def my_badges(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    ubs = db.query(models.UserBadge).filter(models.UserBadge.user_id == current_user.id).all()
    return [
        {
            "id": ub.id,
            "badge_id": ub.badge_id,
            "badge_name": ub.badge.name,
            "badge_icon": ub.badge.icon,
            "badge_description": ub.badge.description,
            "awarded_at": str(ub.awarded_at),
            "awarded_by_name": ub.awarder.name if ub.awarder else "?",
            "note": ub.note,
        }
        for ub in ubs
    ]


@router.get("/user/{user_id}")
def user_badges(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    ubs = db.query(models.UserBadge).filter(models.UserBadge.user_id == user_id).all()
    return [
        {
            "id": ub.id,
            "badge_id": ub.badge_id,
            "badge_name": ub.badge.name,
            "badge_icon": ub.badge.icon,
            "badge_description": ub.badge.description,
            "awarded_at": str(ub.awarded_at),
            "note": ub.note,
        }
        for ub in ubs
    ]
