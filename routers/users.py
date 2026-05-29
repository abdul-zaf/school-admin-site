from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
import models
import security

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "student"


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None


@router.get("/", response_model=List[UserOut])
def list_users(
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    q = db.query(models.User)
    if role:
        q = q.filter(models.User.role == role)
    return q.all()


@router.post("/", response_model=UserOut)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    if data.role not in ("admin", "teacher", "student"):
        raise HTTPException(400, "Invalid role")
    user = models.User(
        name=data.name,
        email=data.email,
        password_hash=security.hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=UserOut)
def get_me(current_user: models.User = Depends(security.get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    if data.name:
        current_user.name = data.name
    if data.password:
        current_user.password_hash = security.hash_password(data.password)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    if user_id == current_user.id:
        raise HTTPException(400, "Cannot delete yourself")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}
