"""
messages.py — Direct messaging between users.

GET    /api/messages/inbox   Received messages for current user
GET    /api/messages/sent    Sent messages from current user
POST   /api/messages/        Send a new message
GET    /api/messages/{id}    Read a single message (marks as read)
DELETE /api/messages/{id}    Delete own message
"""
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


class MessageCreate(BaseModel):
    recipient_id: int
    subject: str
    body: str


@router.get("/")
def inbox(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    msgs = (
        db.query(models.Message)
        .filter(
            models.Message.recipient_id == current_user.id,
            models.Message.deleted_by_recipient == False,
        )
        .order_by(models.Message.sent_at.desc())
        .all()
    )
    return [
        {
            "id": m.id,
            "sender_id": m.sender_id,
            "sender_name": m.sender.name if m.sender else "?",
            "subject": m.subject,
            "body": m.body,
            "sent_at": str(m.sent_at),
            "read_at": str(m.read_at) if m.read_at else None,
            "is_read": m.read_at is not None,
        }
        for m in msgs
    ]


@router.get("/sent")
def sent_messages(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    msgs = (
        db.query(models.Message)
        .filter(
            models.Message.sender_id == current_user.id,
            models.Message.deleted_by_sender == False,
        )
        .order_by(models.Message.sent_at.desc())
        .all()
    )
    return [
        {
            "id": m.id,
            "recipient_id": m.recipient_id,
            "recipient_name": m.recipient.name if m.recipient else "?",
            "subject": m.subject,
            "body": m.body,
            "sent_at": str(m.sent_at),
            "read_at": str(m.read_at) if m.read_at else None,
        }
        for m in msgs
    ]


@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    count = (
        db.query(models.Message)
        .filter(
            models.Message.recipient_id == current_user.id,
            models.Message.deleted_by_recipient == False,
            models.Message.read_at == None,
        )
        .count()
    )
    return {"count": count}


@router.post("/")
def send_message(
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    if data.recipient_id == current_user.id:
        raise HTTPException(400, "You cannot send a message to yourself")
    recipient = db.query(models.User).filter(models.User.id == data.recipient_id).first()
    if not recipient:
        raise HTTPException(404, "Recipient not found")
    msg = models.Message(
        sender_id=current_user.id,
        recipient_id=data.recipient_id,
        subject=data.subject,
        body=data.body,
    )
    db.add(msg)
    notify(db, data.recipient_id, "new_message", f"New message from {current_user.name}",
           data.subject, "/messages")
    db.commit()
    db.refresh(msg)
    return {"id": msg.id, "sent": True}


@router.get("/{message_id}")
def read_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(404, "Message not found")
    if msg.recipient_id != current_user.id and msg.sender_id != current_user.id:
        raise HTTPException(403, "Access denied")
    # Mark as read if recipient
    if msg.recipient_id == current_user.id and msg.read_at is None:
        msg.read_at = datetime.utcnow()
        db.commit()
    return {
        "id": msg.id,
        "sender_id": msg.sender_id,
        "sender_name": msg.sender.name if msg.sender else "?",
        "recipient_id": msg.recipient_id,
        "recipient_name": msg.recipient.name if msg.recipient else "?",
        "subject": msg.subject,
        "body": msg.body,
        "sent_at": str(msg.sent_at),
        "read_at": str(msg.read_at) if msg.read_at else None,
    }


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(404, "Message not found")
    if msg.sender_id == current_user.id:
        msg.deleted_by_sender = True
    elif msg.recipient_id == current_user.id:
        msg.deleted_by_recipient = True
    else:
        raise HTTPException(403, "Access denied")
    db.commit()
    return {"ok": True}
