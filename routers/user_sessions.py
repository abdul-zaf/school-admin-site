"""
user_sessions.py — User session management (token tracking and revocation).

GET    /api/sessions/        List own active sessions
DELETE /api/sessions/all     Revoke all own sessions except current
DELETE /api/sessions/{id}    Revoke a specific session
"""
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
import models
import security

router = APIRouter()

_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def get_or_create_session(token: str, db: Session, request=None) -> Optional[models.UserSession]:
    """Upsert a UserSession record for the given token."""
    token_hash = _hash_token(token)
    sess = db.query(models.UserSession).filter(
        models.UserSession.token_hash == token_hash
    ).first()
    if sess:
        return sess
    # Decode to get user_id
    user = security.get_user_from_token(token, db)
    if not user:
        return None
    ua = None
    ip = None
    if request:
        ua = request.headers.get("user-agent", "")[:500]
        ip = request.client.host if request.client else None
    from datetime import datetime
    sess = models.UserSession(
        user_id=user.id,
        token_hash=token_hash,
        user_agent=ua,
        ip_address=ip,
        created_at=datetime.utcnow(),
        last_used=datetime.utcnow(),
    )
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess


@router.get("/")
def list_sessions(
    token: str = Depends(_oauth2),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    sessions = db.query(models.UserSession).filter(
        models.UserSession.user_id == current_user.id,
        models.UserSession.is_revoked == False,
    ).order_by(models.UserSession.last_used.desc()).all()
    current_hash = _hash_token(token) if token else None
    return [
        {
            "id": s.id,
            "token_preview": s.token_hash[:8],
            "is_current": s.token_hash == current_hash,
            "created_at": str(s.created_at),
            "last_used": str(s.last_used),
            "user_agent": s.user_agent,
            "ip_address": s.ip_address,
        }
        for s in sessions
    ]


@router.delete("/all")
def revoke_all_sessions(
    token: str = Depends(_oauth2),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    current_hash = _hash_token(token) if token else None
    sessions = db.query(models.UserSession).filter(
        models.UserSession.user_id == current_user.id,
        models.UserSession.is_revoked == False,
    ).all()
    revoked = 0
    for s in sessions:
        if s.token_hash != current_hash:
            s.is_revoked = True
            revoked += 1
    db.commit()
    return {"revoked": revoked}


@router.delete("/{session_id}")
def revoke_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    sess = db.query(models.UserSession).filter(
        models.UserSession.id == session_id,
        models.UserSession.user_id == current_user.id,
    ).first()
    if not sess:
        raise HTTPException(404, "Session not found")
    sess.is_revoked = True
    db.commit()
    return {"ok": True}
