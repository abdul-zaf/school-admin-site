"""
clubs.py — Student clubs and club posts.

GET    /api/clubs/                       List clubs
GET    /api/clubs/{id}                   Club detail with members
POST   /api/clubs/                       Create club (teacher/admin)
PUT    /api/clubs/{id}                   Update club (teacher/admin)
DELETE /api/clubs/{id}                  Delete club (admin)
POST   /api/clubs/{id}/join             Join club (student, if is_open)
DELETE /api/clubs/{id}/leave            Leave club (student)
GET    /api/clubs/{id}/posts            List club posts
POST   /api/clubs/{id}/posts            Create post (club member)
DELETE /api/clubs/{id}/posts/{post_id} Delete post (author/admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import security

router = APIRouter()


class ClubCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    teacher_advisor_id: Optional[int] = None
    is_open: bool = True


class ClubUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    teacher_advisor_id: Optional[int] = None
    is_open: Optional[bool] = None


class PostCreate(BaseModel):
    title: str
    content: str


@router.get("/")
def list_clubs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    clubs = db.query(models.StudentClub).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "category": c.category,
            "is_open": c.is_open,
            "member_count": len(c.members),
            "advisor_name": c.advisor.name if c.advisor else None,
        }
        for c in clubs
    ]


@router.get("/{club_id}")
def get_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    club = db.query(models.StudentClub).filter(models.StudentClub.id == club_id).first()
    if not club:
        raise HTTPException(404, "Club not found")
    return {
        "id": club.id,
        "name": club.name,
        "description": club.description,
        "category": club.category,
        "is_open": club.is_open,
        "advisor_name": club.advisor.name if club.advisor else None,
        "members": [
            {
                "user_id": m.user_id,
                "user_name": m.user.name if m.user else None,
                "role": m.role,
                "joined_at": str(m.joined_at),
            }
            for m in club.members
        ],
        "created_at": str(club.created_at),
    }


@router.post("/")
def create_club(
    data: ClubCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("teacher", "admin")),
):
    club = models.StudentClub(
        name=data.name,
        description=data.description,
        category=data.category,
        teacher_advisor_id=data.teacher_advisor_id,
        is_open=data.is_open,
        created_by=current_user.id,
    )
    db.add(club)
    db.commit()
    db.refresh(club)
    return {"id": club.id, "name": club.name}


@router.put("/{club_id}")
def update_club(
    club_id: int,
    data: ClubUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("teacher", "admin")),
):
    club = db.query(models.StudentClub).filter(models.StudentClub.id == club_id).first()
    if not club:
        raise HTTPException(404, "Club not found")
    for field, val in data.model_dump(exclude_none=True).items():
        setattr(club, field, val)
    db.commit()
    return {"ok": True}


@router.delete("/{club_id}")
def delete_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    club = db.query(models.StudentClub).filter(models.StudentClub.id == club_id).first()
    if not club:
        raise HTTPException(404, "Club not found")
    db.delete(club)
    db.commit()
    return {"ok": True}


@router.post("/{club_id}/join")
def join_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    club = db.query(models.StudentClub).filter(models.StudentClub.id == club_id).first()
    if not club:
        raise HTTPException(404, "Club not found")
    if not club.is_open:
        raise HTTPException(400, "Club is not open for new members")
    existing = db.query(models.ClubMember).filter(
        models.ClubMember.club_id == club_id,
        models.ClubMember.user_id == current_user.id,
    ).first()
    if existing:
        raise HTTPException(400, "Already a member")
    m = models.ClubMember(club_id=club_id, user_id=current_user.id, role="member")
    db.add(m)
    db.commit()
    return {"ok": True}


@router.delete("/{club_id}/leave")
def leave_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    m = db.query(models.ClubMember).filter(
        models.ClubMember.club_id == club_id,
        models.ClubMember.user_id == current_user.id,
    ).first()
    if not m:
        raise HTTPException(404, "Not a member of this club")
    db.delete(m)
    db.commit()
    return {"ok": True}


@router.get("/{club_id}/posts")
def list_posts(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    club = db.query(models.StudentClub).filter(models.StudentClub.id == club_id).first()
    if not club:
        raise HTTPException(404, "Club not found")
    posts = db.query(models.ClubPost).filter(
        models.ClubPost.club_id == club_id
    ).order_by(models.ClubPost.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author_id": p.author_id,
            "author_name": p.author.name if p.author else None,
            "created_at": str(p.created_at),
        }
        for p in posts
    ]


@router.post("/{club_id}/posts")
def create_post(
    club_id: int,
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    club = db.query(models.StudentClub).filter(models.StudentClub.id == club_id).first()
    if not club:
        raise HTTPException(404, "Club not found")
    # Must be a member
    membership = db.query(models.ClubMember).filter(
        models.ClubMember.club_id == club_id,
        models.ClubMember.user_id == current_user.id,
    ).first()
    if not membership and current_user.role not in ("admin", "teacher"):
        raise HTTPException(403, "Must be a club member to post")
    post = models.ClubPost(
        club_id=club_id,
        author_id=current_user.id,
        title=data.title,
        content=data.content,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"id": post.id, "title": post.title}


@router.delete("/{club_id}/posts/{post_id}")
def delete_post(
    club_id: int,
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    post = db.query(models.ClubPost).filter(
        models.ClubPost.id == post_id,
        models.ClubPost.club_id == club_id,
    ).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if current_user.role != "admin" and post.author_id != current_user.id:
        raise HTTPException(403, "Not your post")
    db.delete(post)
    db.commit()
    return {"ok": True}
