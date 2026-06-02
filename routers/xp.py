"""
xp.py — XP (experience points) and leveling system.

GET /api/xp/my              Own XP, level, history (student)
GET /api/xp/leaderboard     Top 20 by XP with level
GET /api/xp/{user_id}       Any user's XP (teacher/admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
import security

router = APIRouter()

# XP amounts for each event type
XP_RULES = {
    "submit_assignment": 10,
    "quiz_submission": 15,
    "module_completion": 5,
    "course_completion": 50,
    "teach_back_submission": 20,
    "badge_received": 25,
}

# Level thresholds: level -> min XP
LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 5000, 10000, 20000, 50000]


def _calc_level(total_xp: int) -> int:
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if total_xp >= threshold:
            level = i + 1
    return min(level, 10)


def award_xp(db: Session, user_id: int, event_type: str, description: str = "") -> int:
    """Award XP to a user for an event. Returns XP awarded.
    Caller must db.commit() afterwards.
    """
    xp_amount = XP_RULES.get(event_type, 0)
    if xp_amount == 0:
        return 0

    # Record the event
    event = models.XPEvent(
        user_id=user_id,
        event_type=event_type,
        xp_awarded=xp_amount,
        description=description or event_type,
    )
    db.add(event)

    # Update or create UserXP
    user_xp = db.query(models.UserXP).filter(models.UserXP.user_id == user_id).first()
    if not user_xp:
        user_xp = models.UserXP(user_id=user_id, total_xp=0, level=1)
        db.add(user_xp)
        db.flush()

    user_xp.total_xp += xp_amount
    user_xp.level = _calc_level(user_xp.total_xp)
    user_xp.updated_at = datetime.utcnow()
    return xp_amount


def _xp_detail(user_xp: models.UserXP, history=None):
    next_level_idx = user_xp.level  # 0-indexed into thresholds
    next_threshold = LEVEL_THRESHOLDS[next_level_idx] if next_level_idx < len(LEVEL_THRESHOLDS) else None
    return {
        "total_xp": user_xp.total_xp,
        "level": user_xp.level,
        "next_level_threshold": next_threshold,
        "xp_to_next": (next_threshold - user_xp.total_xp) if next_threshold else None,
        "updated_at": str(user_xp.updated_at),
        **({"history": history} if history is not None else {}),
    }


@router.get("/my")
def my_xp(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    user_xp = db.query(models.UserXP).filter(models.UserXP.user_id == current_user.id).first()
    if not user_xp:
        return {"total_xp": 0, "level": 1, "next_level_threshold": 100, "xp_to_next": 100, "history": []}
    history = (
        db.query(models.XPEvent)
        .filter(models.XPEvent.user_id == current_user.id)
        .order_by(models.XPEvent.created_at.desc())
        .limit(50)
        .all()
    )
    return _xp_detail(user_xp, history=[
        {
            "event_type": e.event_type,
            "xp_awarded": e.xp_awarded,
            "description": e.description,
            "created_at": str(e.created_at),
        }
        for e in history
    ])


@router.get("/leaderboard")
def xp_leaderboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    top = (
        db.query(models.UserXP)
        .order_by(models.UserXP.total_xp.desc())
        .limit(20)
        .all()
    )
    return [
        {
            "rank": i + 1,
            "user_id": ux.user_id,
            "user_name": ux.user.name if ux.user else None,
            "total_xp": ux.total_xp,
            "level": ux.level,
        }
        for i, ux in enumerate(top)
    ]


@router.get("/{user_id}")
def get_user_xp(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    user_xp = db.query(models.UserXP).filter(models.UserXP.user_id == user_id).first()
    if not user_xp:
        return {"user_id": user_id, "total_xp": 0, "level": 1}
    return {"user_id": user_id, "user_name": user.name, **_xp_detail(user_xp)}
