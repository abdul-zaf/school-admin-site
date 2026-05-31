"""
Anonymous peer help board (Stack Overflow style, per course).

Students post questions (anonymous by default).
Other students answer. Everyone can upvote questions and answers.
Teachers can endorse an answer as 'officially correct'.
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

_ANON_NAME = "Anonymous Student"


def _display_name(user: models.User, is_anonymous: bool, viewer: models.User) -> str:
    """Return name or 'Anonymous Student', except teachers/admins always see the real name."""
    if not is_anonymous:
        return user.name
    if viewer.role in ("admin", "teacher"):
        return f"{user.name} (anonymous)"
    return _ANON_NAME


class PostCreate(BaseModel):
    title: str
    body: str
    is_anonymous: bool = True


class AnswerCreate(BaseModel):
    body: str
    is_anonymous: bool = False


# ── Posts ─────────────────────────────────────────────────────────────────────

@router.get("/course/{course_id}")
def list_posts(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    posts = (
        db.query(models.HelpPost)
        .filter(models.HelpPost.course_id == course_id)
        .order_by(models.HelpPost.created_at.desc())
        .all()
    )
    voted_post_ids = {
        v.post_id
        for v in db.query(models.HelpVote)
        .filter(models.HelpVote.voter_id == current_user.id)
        .all()
    }
    return [
        {
            "id":          p.id,
            "title":       p.title,
            "body":        p.body,
            "author":      _display_name(p.author, p.is_anonymous, current_user),
            "is_resolved": p.is_resolved,
            "is_mine":     p.author_id == current_user.id,
            "upvotes":     len(p.votes),
            "has_voted":   p.id in voted_post_ids,
            "answer_count": len(p.answers),
            "created_at":  str(p.created_at),
        }
        for p in posts
    ]


@router.post("/course/{course_id}")
def create_post(
    course_id: int,
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    post = models.HelpPost(
        course_id=course_id,
        author_id=current_user.id,
        is_anonymous=data.is_anonymous,
        title=data.title,
        body=data.body,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"id": post.id}


@router.get("/post/{post_id}")
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    post = db.query(models.HelpPost).filter(models.HelpPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")

    voted_ans_ids = {
        v.answer_id
        for v in db.query(models.HelpAnswerVote)
        .filter(models.HelpAnswerVote.voter_id == current_user.id)
        .all()
    }

    answers = sorted(
        post.answers,
        key=lambda a: (a.is_endorsed, len(a.votes)),
        reverse=True,
    )

    return {
        "id":          post.id,
        "title":       post.title,
        "body":        post.body,
        "author":      _display_name(post.author, post.is_anonymous, current_user),
        "is_resolved": post.is_resolved,
        "is_mine":     post.author_id == current_user.id,
        "upvotes":     len(post.votes),
        "created_at":  str(post.created_at),
        "answers": [
            {
                "id":          a.id,
                "body":        a.body,
                "author":      _display_name(a.author, a.is_anonymous, current_user),
                "is_endorsed": a.is_endorsed,
                "is_mine":     a.author_id == current_user.id,
                "upvotes":     len(a.votes),
                "has_voted":   a.id in voted_ans_ids,
                "created_at":  str(a.created_at),
            }
            for a in answers
        ],
    }


@router.put("/post/{post_id}/resolve")
def resolve_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    post = db.query(models.HelpPost).filter(models.HelpPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != current_user.id and current_user.role not in ("admin", "teacher"):
        raise HTTPException(403, "Not your post")
    post.is_resolved = not post.is_resolved
    db.commit()
    return {"is_resolved": post.is_resolved}


@router.delete("/post/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    post = db.query(models.HelpPost).filter(models.HelpPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != current_user.id and current_user.role not in ("admin", "teacher"):
        raise HTTPException(403, "Not your post")
    db.delete(post)
    db.commit()
    return {"ok": True}


# ── Votes on posts ────────────────────────────────────────────────────────────

@router.post("/post/{post_id}/vote")
def vote_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    post = db.query(models.HelpPost).filter(models.HelpPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    existing = next((v for v in post.votes if v.voter_id == current_user.id), None)
    if existing:
        db.delete(existing)
        db.commit()
        return {"voted": False, "upvotes": len(post.votes) - 1}
    db.add(models.HelpVote(post_id=post_id, voter_id=current_user.id))
    db.commit()
    db.refresh(post)
    return {"voted": True, "upvotes": len(post.votes)}


# ── Answers ───────────────────────────────────────────────────────────────────

@router.post("/post/{post_id}/answer")
def post_answer(
    post_id: int,
    data: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    if not db.query(models.HelpPost).filter(models.HelpPost.id == post_id).first():
        raise HTTPException(404, "Post not found")
    a = models.HelpAnswer(
        post_id=post_id,
        author_id=current_user.id,
        is_anonymous=data.is_anonymous,
        body=data.body,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return {"id": a.id}


@router.post("/answer/{answer_id}/vote")
def vote_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    a = db.query(models.HelpAnswer).filter(models.HelpAnswer.id == answer_id).first()
    if not a:
        raise HTTPException(404, "Answer not found")
    existing = next((v for v in a.votes if v.voter_id == current_user.id), None)
    if existing:
        db.delete(existing)
        db.commit()
        return {"voted": False}
    db.add(models.HelpAnswerVote(answer_id=answer_id, voter_id=current_user.id))
    db.commit()
    return {"voted": True}


@router.post("/answer/{answer_id}/endorse")
def endorse_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    a = db.query(models.HelpAnswer).filter(models.HelpAnswer.id == answer_id).first()
    if not a:
        raise HTTPException(404, "Answer not found")
    a.is_endorsed = not a.is_endorsed
    db.commit()
    return {"is_endorsed": a.is_endorsed}
