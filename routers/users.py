"""
users.py — User account management (admin only, except /me endpoints).

GET    /api/users/        List users (filterable by role)
POST   /api/users/        Create a user account
GET    /api/users/me      Current user profile
PUT    /api/users/me      Update own name or password
DELETE /api/users/{id}    Delete a user (cannot delete self)
POST   /api/users/import  Bulk-import users from CSV

Validation: email normalised to lowercase; password >= 8 chars with
at least one letter and one digit; name 2-100 chars.
"""
import csv
import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional

from database import get_db
import models
import security

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "student"

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        if len(v) > 100:
            raise ValueError("Name must not exceed 100 characters")
        return v

    @field_validator("email")
    @classmethod
    def normalise_email(cls, v: str) -> str:
        """Lower-case and strip so 'User@School.edu' == 'user@school.edu'."""
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def validate_pw(cls, v: str) -> str:
        return security.validate_password(v)


class UserOut(BaseModel):
    """Public representation of a user — never includes the password hash."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if len(v) < 2:
                raise ValueError("Name must be at least 2 characters")
            if len(v) > 100:
                raise ValueError("Name must not exceed 100 characters")
        return v

    @field_validator("password")
    @classmethod
    def validate_pw(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return security.validate_password(v)
        return v


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[UserOut])
def list_users(
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    q = db.query(models.User)
    if current_user.role == "teacher":
        # Teachers can only see teacher accounts
        q = q.filter(models.User.role == "teacher")
    elif role:
        q = q.filter(models.User.role == role)
    return q.all()


@router.post("/", response_model=UserOut)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    if current_user.role == "teacher":
        # Teachers can only create teacher accounts
        if data.role != "teacher":
            raise HTTPException(403, "Teachers can only create teacher accounts")
    elif data.role not in ("admin", "teacher", "student", "parent"):
        raise HTTPException(400, "Invalid role — must be admin, teacher, student, or parent")
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
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


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if current_user.role == "teacher" and user.role != "teacher":
        raise HTTPException(403, "Teachers can only view teacher accounts")
    return user


@router.put("/me", response_model=UserOut)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    if data.name is not None:
        current_user.name = data.name
    if data.password is not None:
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
        raise HTTPException(400, "Cannot delete your own account")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}


@router.post("/import")
async def bulk_import_users(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    """Bulk import users from CSV. Expected columns: name,email,password,role"""
    content = await file.read()
    text = content.decode("utf-8-sig")  # handle BOM
    reader = csv.DictReader(io.StringIO(text))

    created = []
    errors = []
    for i, row in enumerate(reader, start=2):  # row 1 = header
        try:
            name = row.get("name", "").strip()
            email = row.get("email", "").strip().lower()
            password = row.get("password", "").strip()
            role = row.get("role", "student").strip()

            if not name or not email or not password:
                errors.append({"row": i, "error": "Missing required field"})
                continue
            if role not in ("admin", "teacher", "student", "parent"):
                errors.append({"row": i, "error": f"Invalid role: {role}"})
                continue

            try:
                security.validate_password(password)
            except ValueError as e:
                errors.append({"row": i, "error": str(e)})
                continue

            if db.query(models.User).filter(models.User.email == email).first():
                errors.append({"row": i, "error": f"Email already exists: {email}"})
                continue

            user = models.User(
                name=name,
                email=email,
                password_hash=security.hash_password(password),
                role=role,
            )
            db.add(user)
            db.flush()
            created.append({"email": email, "role": role})
        except Exception as e:
            errors.append({"row": i, "error": str(e)})

    db.commit()
    return {"created": len(created), "errors": errors, "users": created}
