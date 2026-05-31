"""
Teach-it-back: teachers set a concept to explain; students submit their own
explanation in plain text; peers upvote the best ones; teachers score & give feedback.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
import models
import security

router = APIRouter()


class PromptCreate(BaseModel):
    concept: str
    description: Optional[str] = None


class ExplanationSubmit(BaseModel):
    explanation: str


class GradeSubmit(BaseModel):
    score: float          # 0-100
    feedback: Optional[str] = None


# ── Prompts ───────────────────────────────────────────────────────────────────

@router.get("/course/{course_id}")
def list_prompts(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    prompts = (
        db.query(models.TeachBackPrompt)
        .filter(models.TeachBackPrompt.course_id == course_id)
        .order_by(models.TeachBackPrompt.created_at.desc())
        .all()
    )
    result = []
    for p in prompts:
        my_sub = None
        if current_user.role == "student":
            s = next((s for s in p.submissions if s.student_id == current_user.id), None)
            if s:
                my_sub = {
                    "id": s.id, "explanation": s.explanation,
                    "score": s.score, "feedback": s.feedback,
                    "upvotes": len(s.votes),
                }
        result.append({
            "id":          p.id,
            "concept":     p.concept,
            "description": p.description,
            "created_at":  str(p.created_at),
            "teacher_name": p.teacher.name if p.teacher else None,
            "submission_count": len(p.submissions),
            "my_submission": my_sub,
        })
    return result


@router.post("/course/{course_id}")
def create_prompt(
    course_id: int,
    data: PromptCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    p = models.TeachBackPrompt(
        course_id=course_id, teacher_id=current_user.id,
        concept=data.concept, description=data.description,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "concept": p.concept}


@router.delete("/{prompt_id}")
def delete_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    p = db.query(models.TeachBackPrompt).filter(models.TeachBackPrompt.id == prompt_id).first()
    if not p:
        raise HTTPException(404, "Prompt not found")
    security.require_course_access(p.course_id, current_user, db)
    db.delete(p)
    db.commit()
    return {"ok": True}


# ── Submissions ───────────────────────────────────────────────────────────────

@router.get("/{prompt_id}/submissions")
def list_submissions(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    p = db.query(models.TeachBackPrompt).filter(models.TeachBackPrompt.id == prompt_id).first()
    if not p:
        raise HTTPException(404, "Prompt not found")

    voted_ids = set()
    if current_user.role == "student":
        voted_ids = {
            v.submission_id
            for v in db.query(models.TeachBackVote)
            .filter(models.TeachBackVote.voter_id == current_user.id)
            .all()
        }

    return [
        {
            "id":          s.id,
            "student_name": s.student.name if s.student else "?",
            "explanation": s.explanation,
            "score":       s.score,
            "feedback":    s.feedback,
            "upvotes":     len(s.votes),
            "submitted_at": str(s.submitted_at),
            "has_voted":   s.id in voted_ids,
            "is_mine":     s.student_id == current_user.id,
        }
        for s in sorted(p.submissions, key=lambda x: len(x.votes), reverse=True)
    ]


@router.post("/{prompt_id}/submit")
def submit_explanation(
    prompt_id: int,
    data: ExplanationSubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    p = db.query(models.TeachBackPrompt).filter(models.TeachBackPrompt.id == prompt_id).first()
    if not p:
        raise HTTPException(404, "Prompt not found")
    existing = next((s for s in p.submissions if s.student_id == current_user.id), None)
    if existing:
        existing.explanation  = data.explanation
        existing.submitted_at = datetime.utcnow()
        db.commit()
        return {"id": existing.id, "resubmitted": True}
    s = models.TeachBackSubmission(
        prompt_id=prompt_id, student_id=current_user.id, explanation=data.explanation,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id, "submitted": True}


@router.post("/submissions/{submission_id}/vote")
def vote_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    s = db.query(models.TeachBackSubmission).filter(
        models.TeachBackSubmission.id == submission_id
    ).first()
    if not s:
        raise HTTPException(404, "Submission not found")
    if s.student_id == current_user.id:
        raise HTTPException(400, "Cannot vote on your own submission")
    existing = next((v for v in s.votes if v.voter_id == current_user.id), None)
    if existing:
        db.delete(existing)
        db.commit()
        return {"voted": False}
    db.add(models.TeachBackVote(submission_id=submission_id, voter_id=current_user.id))
    db.commit()
    return {"voted": True}


@router.put("/submissions/{submission_id}/grade")
def grade_submission(
    submission_id: int,
    data: GradeSubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    s = db.query(models.TeachBackSubmission).filter(
        models.TeachBackSubmission.id == submission_id
    ).first()
    if not s:
        raise HTTPException(404, "Submission not found")
    security.require_course_access(s.prompt.course_id, current_user, db)
    s.score    = data.score
    s.feedback = data.feedback
    db.commit()
    return {"ok": True}
