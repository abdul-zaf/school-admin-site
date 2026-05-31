"""
Spaced Repetition (SM-2 algorithm).

Cards are created automatically when a student answers a quiz question incorrectly.
Students can review their due cards from the dashboard.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
import models
import security

router = APIRouter()


# ── SM-2 core ────────────────────────────────────────────────────────────────

def _sm2_update(card: models.SRCard, quality: int) -> models.SRCard:
    """
    Update a card using the SM-2 algorithm.
    quality: 0-5  (0=blackout, 3=correct with difficulty, 5=perfect recall)
    """
    if quality < 3:
        card.repetitions = 0
        card.interval    = 1
    else:
        if card.repetitions == 0:
            card.interval = 1
        elif card.repetitions == 1:
            card.interval = 6
        else:
            card.interval = max(1, round(card.interval * card.ease_factor))
        card.repetitions += 1

    # Update ease factor (clamped to ≥ 1.3)
    card.ease_factor = max(
        1.3,
        card.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02),
    )
    card.due_date      = datetime.utcnow() + timedelta(days=card.interval)
    card.last_reviewed = datetime.utcnow()
    card.last_quality  = quality
    return card


def _get_or_create_card(student_id: int, question_id: int, db: Session) -> models.SRCard:
    card = (
        db.query(models.SRCard)
        .filter(
            models.SRCard.student_id  == student_id,
            models.SRCard.question_id == question_id,
        )
        .first()
    )
    if not card:
        card = models.SRCard(student_id=student_id, question_id=question_id)
        db.add(card)
        db.flush()
    return card


# ── Called internally when a quiz is submitted ───────────────────────────────

def enqueue_wrong_answers(attempt: models.QuizAttempt, db: Session):
    """
    Create / refresh SR cards for every question the student got wrong in
    this quiz attempt.  Call this after grading inside the quizzes router.
    """
    for answer in attempt.answers:
        q = answer.question
        if q.question_type == "short_answer":
            continue  # can't auto-assess short answers
        correct = any(o.is_correct for o in q.options if o.id == answer.selected_option_id)
        if not correct:
            card = _get_or_create_card(attempt.student_id, q.id, db)
            # Treat an incorrect first encounter as quality=1 (wrong but seen)
            _sm2_update(card, quality=1)
    db.flush()


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/due")
def get_due_cards(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    """Return all SR cards due for review today, with question text and options."""
    now = datetime.utcnow()
    cards = (
        db.query(models.SRCard)
        .filter(
            models.SRCard.student_id == current_user.id,
            models.SRCard.due_date   <= now,
        )
        .all()
    )
    result = []
    for c in cards:
        q = c.question
        result.append({
            "card_id":       c.id,
            "question_id":   q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options": [
                {"id": o.id, "option_text": o.option_text}
                for o in q.options
            ],
            "interval":     c.interval,
            "repetitions":  c.repetitions,
            "last_quality": c.last_quality,
        })
    return result


class ReviewSubmit(BaseModel):
    quality: int          # 0-5


@router.post("/{card_id}/review")
def submit_review(
    card_id: int,
    data: ReviewSubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    """Record the student's self-assessment and advance the card's schedule."""
    if data.quality < 0 or data.quality > 5:
        raise HTTPException(400, "quality must be 0-5")

    card = (
        db.query(models.SRCard)
        .filter(
            models.SRCard.id         == card_id,
            models.SRCard.student_id == current_user.id,
        )
        .first()
    )
    if not card:
        raise HTTPException(404, "Card not found")

    _sm2_update(card, data.quality)
    db.commit()
    return {
        "next_review_in_days": card.interval,
        "ease_factor":         round(card.ease_factor, 2),
        "repetitions":         card.repetitions,
    }


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    """Summary stats for the student's SR deck."""
    now = datetime.utcnow()
    all_cards = (
        db.query(models.SRCard)
        .filter(models.SRCard.student_id == current_user.id)
        .all()
    )
    due_today = sum(1 for c in all_cards if c.due_date <= now)
    mastered  = sum(1 for c in all_cards if c.repetitions >= 5)
    return {
        "total":     len(all_cards),
        "due_today": due_today,
        "mastered":  mastered,
        "learning":  len(all_cards) - mastered,
    }
