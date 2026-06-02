"""
streaks.py — Daily activity streak tracking.

GET /api/streaks/my           Get own streak info (student)
GET /api/streaks/leaderboard  Top 10 streaks
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from database import get_db
import models
import security

router = APIRouter()


def record_activity(db: Session, user_id: int):
    """Record a daily activity event and update the student's streak.
    Call this whenever a student submits an assignment, attempts a quiz, or completes a module.
    Caller is responsible for db.commit() after calling this.
    """
    today = date.today()
    # Upsert DailyActivity
    existing = db.query(models.DailyActivity).filter(
        models.DailyActivity.user_id == user_id,
        models.DailyActivity.activity_date == today,
    ).first()
    if not existing:
        db.add(models.DailyActivity(user_id=user_id, activity_date=today))

    # Update streak
    streak = db.query(models.StudentStreak).filter(
        models.StudentStreak.user_id == user_id
    ).first()
    if not streak:
        streak = models.StudentStreak(user_id=user_id, current_streak=1, longest_streak=1, last_activity_date=today)
        db.add(streak)
    else:
        if streak.last_activity_date == today:
            return  # already recorded today
        yesterday = today - timedelta(days=1)
        if streak.last_activity_date == yesterday:
            streak.current_streak += 1
        else:
            streak.current_streak = 1
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
        streak.last_activity_date = today
        streak.updated_at = datetime.utcnow()


@router.get("/my")
def my_streak(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    streak = db.query(models.StudentStreak).filter(
        models.StudentStreak.user_id == current_user.id
    ).first()
    if not streak:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "last_activity_date": None,
        }
    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "last_activity_date": str(streak.last_activity_date) if streak.last_activity_date else None,
        "updated_at": str(streak.updated_at),
    }


@router.get("/leaderboard")
def streak_leaderboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    top = (
        db.query(models.StudentStreak)
        .order_by(models.StudentStreak.current_streak.desc())
        .limit(10)
        .all()
    )
    return [
        {
            "rank": i + 1,
            "user_id": s.user_id,
            "user_name": s.user.name if s.user else None,
            "current_streak": s.current_streak,
            "longest_streak": s.longest_streak,
        }
        for i, s in enumerate(top)
    ]
