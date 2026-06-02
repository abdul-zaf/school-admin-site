"""
audit.py — Audit log router built on the existing ActivityLog model.

GET /api/audit/    Paginated audit log with filters (admin only)
GET /api/audit/my  User's own activity log
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
import models
import security

router = APIRouter()


def log_activity(db: Session, user_id: int, action_type: str, course_id: Optional[int] = None):
    """Helper to write an ActivityLog entry."""
    entry = models.ActivityLog(
        user_id=user_id,
        course_id=course_id,
        action_type=action_type,
    )
    db.add(entry)
    # Note: caller is responsible for db.commit()


@router.get("/")
def list_audit_log(
    user_id: Optional[int] = None,
    course_id: Optional[int] = None,
    action_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    q = db.query(models.ActivityLog)
    if user_id:
        q = q.filter(models.ActivityLog.user_id == user_id)
    if course_id:
        q = q.filter(models.ActivityLog.course_id == course_id)
    if action_type:
        q = q.filter(models.ActivityLog.action_type == action_type)
    total = q.count()
    logs = q.order_by(models.ActivityLog.created_at.desc()).offset(offset).limit(limit).all()
    # Eagerly load user names
    user_cache = {}
    for log in logs:
        if log.user_id not in user_cache:
            u = db.query(models.User).filter(models.User.id == log.user_id).first()
            user_cache[log.user_id] = u.name if u else "Unknown"
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "logs": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "user_name": user_cache.get(log.user_id),
                "course_id": log.course_id,
                "action_type": log.action_type,
                "created_at": str(log.created_at),
            }
            for log in logs
        ],
    }


@router.get("/my")
def my_activity(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    logs = (
        db.query(models.ActivityLog)
        .filter(models.ActivityLog.user_id == current_user.id)
        .order_by(models.ActivityLog.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": log.id,
            "course_id": log.course_id,
            "action_type": log.action_type,
            "created_at": str(log.created_at),
        }
        for log in logs
    ]
