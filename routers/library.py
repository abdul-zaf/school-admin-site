"""
library.py — Library management system.

GET    /api/library/                    List/search books
GET    /api/library/my-borrows          Own borrows (student)
GET    /api/library/borrows             All borrows (admin), ?overdue=true
GET    /api/library/{id}               Book detail
POST   /api/library/                   Add book (admin)
PUT    /api/library/{id}               Update book (admin)
DELETE /api/library/{id}               Delete book (admin)
POST   /api/library/{id}/borrow        Borrow book (student)
POST   /api/library/borrows/{id}/return Return book (student/admin)
POST   /api/library/borrows/{id}/renew  Renew borrow (student)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from database import get_db
import models
import security

router = APIRouter()

BORROW_DAYS = 14
MAX_RENEWALS = 2


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    description: Optional[str] = None
    category: str
    total_copies: int = 1
    cover_url: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    total_copies: Optional[int] = None
    cover_url: Optional[str] = None


def _book_dict(b: models.LibraryBook):
    return {
        "id": b.id,
        "title": b.title,
        "author": b.author,
        "isbn": b.isbn,
        "description": b.description,
        "category": b.category,
        "total_copies": b.total_copies,
        "available_copies": b.available_copies,
        "cover_url": b.cover_url,
        "created_at": str(b.created_at),
    }


@router.get("/my-borrows")
def my_borrows(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    borrows = db.query(models.LibraryBorrow).filter(
        models.LibraryBorrow.borrower_id == current_user.id
    ).order_by(models.LibraryBorrow.borrowed_at.desc()).all()
    return [
        {
            "id": b.id,
            "book_id": b.book_id,
            "book_title": b.book.title if b.book else None,
            "borrowed_at": str(b.borrowed_at),
            "due_date": str(b.due_date),
            "returned_at": str(b.returned_at) if b.returned_at else None,
            "renewed_count": b.renewed_count,
            "overdue": b.returned_at is None and datetime.utcnow() > b.due_date,
        }
        for b in borrows
    ]


@router.get("/borrows")
def all_borrows(
    overdue: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    q = db.query(models.LibraryBorrow)
    if overdue:
        now = datetime.utcnow()
        q = q.filter(models.LibraryBorrow.returned_at == None, models.LibraryBorrow.due_date < now)
    borrows = q.order_by(models.LibraryBorrow.borrowed_at.desc()).all()
    return [
        {
            "id": b.id,
            "book_id": b.book_id,
            "book_title": b.book.title if b.book else None,
            "borrower_id": b.borrower_id,
            "borrower_name": b.borrower.name if b.borrower else None,
            "borrowed_at": str(b.borrowed_at),
            "due_date": str(b.due_date),
            "returned_at": str(b.returned_at) if b.returned_at else None,
            "renewed_count": b.renewed_count,
        }
        for b in borrows
    ]


@router.get("/")
def list_books(
    q: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    query = db.query(models.LibraryBook)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.LibraryBook.title.ilike(like)) |
            (models.LibraryBook.author.ilike(like)) |
            (models.LibraryBook.isbn.ilike(like))
        )
    if category:
        query = query.filter(models.LibraryBook.category == category)
    return [_book_dict(b) for b in query.order_by(models.LibraryBook.title).all()]


@router.get("/{book_id}")
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    book = db.query(models.LibraryBook).filter(models.LibraryBook.id == book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")
    return _book_dict(book)


@router.post("/")
def add_book(
    data: BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    book = models.LibraryBook(
        title=data.title,
        author=data.author,
        isbn=data.isbn,
        description=data.description,
        category=data.category,
        total_copies=data.total_copies,
        available_copies=data.total_copies,
        cover_url=data.cover_url,
        added_by=current_user.id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"id": book.id, "title": book.title}


@router.put("/{book_id}")
def update_book(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    book = db.query(models.LibraryBook).filter(models.LibraryBook.id == book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")
    for field, val in data.model_dump(exclude_none=True).items():
        setattr(book, field, val)
    db.commit()
    return {"ok": True}


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    book = db.query(models.LibraryBook).filter(models.LibraryBook.id == book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")
    db.delete(book)
    db.commit()
    return {"ok": True}


@router.post("/{book_id}/borrow")
def borrow_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    book = db.query(models.LibraryBook).filter(models.LibraryBook.id == book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")
    if book.available_copies <= 0:
        raise HTTPException(400, "No copies available")
    # Check if already borrowing this book
    active = db.query(models.LibraryBorrow).filter(
        models.LibraryBorrow.book_id == book_id,
        models.LibraryBorrow.borrower_id == current_user.id,
        models.LibraryBorrow.returned_at == None,
    ).first()
    if active:
        raise HTTPException(400, "You already have this book borrowed")
    book.available_copies -= 1
    now = datetime.utcnow()
    borrow = models.LibraryBorrow(
        book_id=book_id,
        borrower_id=current_user.id,
        borrowed_at=now,
        due_date=now + timedelta(days=BORROW_DAYS),
    )
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return {"id": borrow.id, "due_date": str(borrow.due_date)}


@router.post("/borrows/{borrow_id}/return")
def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    borrow = db.query(models.LibraryBorrow).filter(models.LibraryBorrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(404, "Borrow record not found")
    if current_user.role == "student" and borrow.borrower_id != current_user.id:
        raise HTTPException(403, "Not your borrow record")
    if borrow.returned_at:
        raise HTTPException(400, "Already returned")
    borrow.returned_at = datetime.utcnow()
    borrow.book.available_copies += 1
    db.commit()
    return {"ok": True, "returned_at": str(borrow.returned_at)}


@router.post("/borrows/{borrow_id}/renew")
def renew_borrow(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    borrow = db.query(models.LibraryBorrow).filter(
        models.LibraryBorrow.id == borrow_id,
        models.LibraryBorrow.borrower_id == current_user.id,
    ).first()
    if not borrow:
        raise HTTPException(404, "Borrow record not found")
    if borrow.returned_at:
        raise HTTPException(400, "Book already returned")
    if borrow.renewed_count >= MAX_RENEWALS:
        raise HTTPException(400, f"Maximum renewals ({MAX_RENEWALS}) reached")
    borrow.due_date = borrow.due_date + timedelta(days=BORROW_DAYS)
    borrow.renewed_count += 1
    db.commit()
    return {"ok": True, "new_due_date": str(borrow.due_date), "renewed_count": borrow.renewed_count}
