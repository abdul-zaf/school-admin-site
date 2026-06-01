"""
auth.py — Login endpoint.

POST /api/auth/login
  Accepts OAuth2 password form (username = email).
  Returns a JWT access token valid for 24 hours.
  Rate-limited to 10 attempts per IP per 60 seconds.
  Uses a dummy bcrypt hash for unknown emails to prevent timing-based
  user enumeration.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
import models
import security

router = APIRouter()


@router.post("/login")
def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # ── Rate limiting (per client IP) ────────────────────────────────────────
    client_ip = request.client.host if request.client else "unknown"
    if not security.login_limiter.is_allowed(f"login:{client_ip}"):
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Please wait a minute and try again.",
            headers={"Retry-After": "60"},
        )

    # Normalise email before lookup
    email = form.username.strip().lower()
    user = db.query(models.User).filter(models.User.email == email).first()

    # Always run bcrypt — prevents timing-based user-enumeration attacks.
    # If the user doesn't exist we verify against a dummy hash so the response
    # time is the same whether the email is registered or not.
    candidate_hash = user.password_hash if user else security.DUMMY_HASH
    password_ok = security.verify_password(form.password, candidate_hash)

    if not user or not password_ok:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "access_token": security.create_token(user.id),
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name,
        "role": user.role,
    }
