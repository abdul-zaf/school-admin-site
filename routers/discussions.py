"""
discussions.py — Per-course discussion boards and threaded posts.

GET    /api/discussions/course/{id}            List boards for a course
POST   /api/discussions/course/{id}            Create a board (teacher/admin)
DELETE /api/discussions/boards/{id}            Delete a board
GET    /api/discussions/boards/{id}/posts      List posts in a board
POST   /api/discussions/boards/{id}/posts      Create a post
DELETE /api/discussions/posts/{id}             Delete own post (or admin)
POST   /api/discussions/posts/{id}/reply       Reply to a post
POST   /api/discussions/posts/{id}/endorse     Teacher endorses a post
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


class BoardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_pinned: bool = False


class PostCreate(BaseModel):
    content: str


@router.get("/course/{course_id}")
def list_boards(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    boards = (
        db.query(models.DiscussionBoard)
        .filter(models.DiscussionBoard.course_id == course_id)
        .order_by(models.DiscussionBoard.is_pinned.desc(), models.DiscussionBoard.created_at.desc())
        .all()
    )
    return [
        {
            "id": b.id,
            "course_id": b.course_id,
            "title": b.title,
            "description": b.description,
            "is_pinned": b.is_pinned,
            "created_by": b.created_by,
            "created_at": str(b.created_at),
            "post_count": len(b.posts),
        }
        for b in boards
    ]


@router.post("/course/{course_id}")
def create_board(
    course_id: int,
    data: BoardCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    board = models.DiscussionBoard(
        course_id=course_id,
        title=data.title,
        description=data.description,
        is_pinned=data.is_pinned,
        created_by=current_user.id,
    )
    db.add(board)
    db.commit()
    db.refresh(board)
    return {"id": board.id, "title": board.title}


@router.delete("/boards/{board_id}")
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    board = db.query(models.DiscussionBoard).filter(models.DiscussionBoard.id == board_id).first()
    if not board:
        raise HTTPException(404, "Board not found")
    security.require_course_access(board.course_id, current_user, db)
    db.delete(board)
    db.commit()
    return {"ok": True}


def _serialize_post(p, depth=0):
    result = {
        "id": p.id,
        "board_id": p.board_id,
        "author_id": p.author_id,
        "author_name": p.author.name if p.author else "?",
        "parent_id": p.parent_id,
        "content": p.content,
        "is_endorsed": p.is_endorsed,
        "created_at": str(p.created_at),
        "replies": [],
    }
    if depth < 5:  # limit recursion depth
        result["replies"] = [_serialize_post(r, depth + 1) for r in p.replies]
    return result


@router.get("/boards/{board_id}/posts")
def list_posts(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    board = db.query(models.DiscussionBoard).filter(models.DiscussionBoard.id == board_id).first()
    if not board:
        raise HTTPException(404, "Board not found")
    # Return top-level posts with nested replies
    top_level = (
        db.query(models.DiscussionPost)
        .filter(
            models.DiscussionPost.board_id == board_id,
            models.DiscussionPost.parent_id == None,
        )
        .order_by(models.DiscussionPost.created_at.asc())
        .all()
    )
    return [_serialize_post(p) for p in top_level]


@router.post("/boards/{board_id}/posts")
def create_post(
    board_id: int,
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    board = db.query(models.DiscussionBoard).filter(models.DiscussionBoard.id == board_id).first()
    if not board:
        raise HTTPException(404, "Board not found")
    post = models.DiscussionPost(
        board_id=board_id,
        author_id=current_user.id,
        content=data.content,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"id": post.id}


@router.post("/posts/{post_id}/reply")
def reply_to_post(
    post_id: int,
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    parent = db.query(models.DiscussionPost).filter(models.DiscussionPost.id == post_id).first()
    if not parent:
        raise HTTPException(404, "Post not found")
    reply = models.DiscussionPost(
        board_id=parent.board_id,
        author_id=current_user.id,
        parent_id=post_id,
        content=data.content,
    )
    db.add(reply)
    # Notify original author
    if parent.author_id != current_user.id:
        notify(db, parent.author_id, "discussion_reply", f"{current_user.name} replied to your post",
               data.content[:100], f"/board/{parent.board_id}")
    db.commit()
    db.refresh(reply)
    return {"id": reply.id}


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    post = db.query(models.DiscussionPost).filter(models.DiscussionPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if current_user.role not in ("admin", "teacher") and post.author_id != current_user.id:
        raise HTTPException(403, "Cannot delete another user's post")
    db.delete(post)
    db.commit()
    return {"ok": True}


@router.put("/posts/{post_id}/endorse")
def endorse_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    post = db.query(models.DiscussionPost).filter(models.DiscussionPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    post.is_endorsed = not post.is_endorsed
    db.commit()
    return {"is_endorsed": post.is_endorsed}
