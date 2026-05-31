"""
Live confusion heatmap.

Students tap 'confused' or 'clear' during a session.
Teacher polls the endpoint to see the rolling counts.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
import models
import security

router = APIRouter()

# Only count signals from the last N minutes to keep the heatmap "live"
_WINDOW_MINUTES = 10


class SignalSubmit(BaseModel):
    signal: str   # "confused" | "clear"


@router.post("/{session_id}/signal")
def send_signal(
    session_id: int,
    data: SignalSubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    if data.signal not in ("confused", "clear"):
        raise HTTPException(400, "signal must be 'confused' or 'clear'")

    # Upsert: one active signal per student per session
    existing = (
        db.query(models.ConfusionSignal)
        .filter(
            models.ConfusionSignal.session_id == session_id,
            models.ConfusionSignal.student_id == current_user.id,
        )
        .first()
    )
    if existing:
        existing.signal     = data.signal
        existing.created_at = datetime.utcnow()
    else:
        db.add(models.ConfusionSignal(
            session_id=session_id,
            student_id=current_user.id,
            signal=data.signal,
        ))
    db.commit()
    return {"ok": True}


@router.get("/{session_id}/stats")
def get_stats(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    """
    Returns rolling counts for the last 10 minutes.
    Accessible by teachers/admins; students see only their own signal.
    """
    session = db.query(models.ClassSession).filter(
        models.ClassSession.id == session_id
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")

    cutoff  = datetime.utcnow() - timedelta(minutes=_WINDOW_MINUTES)
    signals = (
        db.query(models.ConfusionSignal)
        .filter(
            models.ConfusionSignal.session_id == session_id,
            models.ConfusionSignal.created_at >= cutoff,
        )
        .all()
    )

    confused = sum(1 for s in signals if s.signal == "confused")
    clear    = sum(1 for s in signals if s.signal == "clear")
    total    = confused + clear

    if current_user.role == "student":
        my = next((s for s in signals if s.student_id == current_user.id), None)
        return {"my_signal": my.signal if my else None}

    return {
        "confused":       confused,
        "clear":          clear,
        "total_signals":  total,
        "confusion_pct":  round(confused / total * 100) if total else 0,
        "window_minutes": _WINDOW_MINUTES,
    }


@router.delete("/{session_id}/clear")
def clear_signals(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Teacher clears all signals to reset the heatmap."""
    db.query(models.ConfusionSignal).filter(
        models.ConfusionSignal.session_id == session_id
    ).delete()
    db.commit()
    return {"ok": True}
