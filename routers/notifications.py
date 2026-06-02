"""
notifications.py — In-app notification bell.

GET   /api/notifications/              List recent notifications
GET   /api/notifications/unread-count  Unread count (polled by frontend)
PUT   /api/notifications/{id}/read     Mark a notification as read
PATCH /api/notifications/email-preferences Toggle email_notifications for user
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models
import security

router = APIRouter()


class EmailPreferences(BaseModel):
    email_notifications: bool


def notify(db: Session, user_id: int, type: str, title: str, body: str = "", link: str = ""):
    """Helper to create a notification. Importable by other routers."""
    n = models.Notification(
        user_id=user_id,
        type=type,
        title=title,
        body=body,
        link=link,
        is_read=False,
    )
    db.add(n)
    # Note: caller must commit


@router.get("/")
def get_notifications(
    skip: int = 0,
    limit: int = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    notifs = (
        db.query(models.Notification)
        .filter(models.Notification.user_id == current_user.id)
        .order_by(models.Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": n.id,
            "type": n.type,
            "title": n.title,
            "body": n.body,
            "link": n.link,
            "is_read": n.is_read,
            "created_at": str(n.created_at),
        }
        for n in notifs
    ]


@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    count = (
        db.query(models.Notification)
        .filter(
            models.Notification.user_id == current_user.id,
            models.Notification.is_read == False,
        )
        .count()
    )
    return {"count": count}


@router.put("/{notif_id}/read")
def mark_one_read(
    notif_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    n = db.query(models.Notification).filter(
        models.Notification.id == notif_id,
        models.Notification.user_id == current_user.id,
    ).first()
    if not n:
        raise HTTPException(404, "Notification not found")
    n.is_read = True
    db.commit()
    return {"ok": True}


@router.put("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.is_read == False,
    ).update({"is_read": True})
    db.commit()
    return {"ok": True}


@router.patch("/email-preferences")
def set_email_preferences(
    data: EmailPreferences,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    current_user.email_notifications = data.email_notifications
    db.commit()
    return {"email_notifications": current_user.email_notifications}
