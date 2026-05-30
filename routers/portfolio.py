from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models
import security

router = APIRouter()


class PortfolioUpdate(BaseModel):
    title: Optional[str] = None
    bio: Optional[str] = None
    is_public: Optional[bool] = None


class PortfolioItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[str] = None


def get_or_create_portfolio(student_id: int, db: Session) -> models.Portfolio:
    portfolio = db.query(models.Portfolio).filter(
        models.Portfolio.student_id == student_id
    ).first()
    if not portfolio:
        portfolio = models.Portfolio(
            student_id=student_id,
            title="My Portfolio",
            is_public=False,
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
    return portfolio


@router.get("/my")
def get_my_portfolio(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    portfolio = get_or_create_portfolio(current_user.id, db)
    return {
        "id": portfolio.id,
        "student_id": portfolio.student_id,
        "title": portfolio.title,
        "bio": portfolio.bio,
        "is_public": portfolio.is_public,
        "updated_at": str(portfolio.updated_at) if portfolio.updated_at else None,
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "content": item.content,
                "url": item.url,
                "tags": item.tags,
                "created_at": str(item.created_at),
            }
            for item in portfolio.items
        ],
    }


@router.put("/my")
def update_my_portfolio(
    data: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    portfolio = get_or_create_portfolio(current_user.id, db)
    if data.title is not None:
        portfolio.title = data.title
    if data.bio is not None:
        portfolio.bio = data.bio
    if data.is_public is not None:
        portfolio.is_public = data.is_public
    portfolio.updated_at = datetime.utcnow()
    db.commit()
    return {"ok": True}


@router.post("/my/items")
def add_portfolio_item(
    data: PortfolioItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    portfolio = get_or_create_portfolio(current_user.id, db)
    item = models.PortfolioItem(
        portfolio_id=portfolio.id,
        title=data.title,
        description=data.description,
        content=data.content,
        url=data.url,
        tags=data.tags,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "title": item.title}


@router.put("/items/{item_id}")
def update_portfolio_item(
    item_id: int,
    data: PortfolioItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    item = db.query(models.PortfolioItem).filter(models.PortfolioItem.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")
    if item.portfolio.student_id != current_user.id:
        raise HTTPException(403, "Not your portfolio")
    item.title = data.title
    if data.description is not None:
        item.description = data.description
    if data.content is not None:
        item.content = data.content
    if data.url is not None:
        item.url = data.url
    if data.tags is not None:
        item.tags = data.tags
    db.commit()
    return {"ok": True}


@router.delete("/items/{item_id}")
def delete_portfolio_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    item = db.query(models.PortfolioItem).filter(models.PortfolioItem.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")
    if item.portfolio.student_id != current_user.id:
        raise HTTPException(403, "Not your portfolio")
    db.delete(item)
    db.commit()
    return {"ok": True}


@router.get("/{student_id}")
def view_portfolio(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    portfolio = db.query(models.Portfolio).filter(
        models.Portfolio.student_id == student_id
    ).first()
    if not portfolio:
        raise HTTPException(404, "Portfolio not found")

    # Only show if public, or if teacher/admin, or own portfolio
    if not portfolio.is_public and current_user.role not in ("admin", "teacher"):
        if current_user.id != student_id:
            raise HTTPException(403, "This portfolio is private")

    return {
        "id": portfolio.id,
        "student_id": portfolio.student_id,
        "title": portfolio.title,
        "bio": portfolio.bio,
        "is_public": portfolio.is_public,
        "updated_at": str(portfolio.updated_at) if portfolio.updated_at else None,
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "content": item.content,
                "url": item.url,
                "tags": item.tags,
                "created_at": str(item.created_at),
            }
            for item in portfolio.items
        ],
    }
