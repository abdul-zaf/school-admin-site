"""
security.py — Authentication, authorisation, and rate-limiting utilities.
"""
import os
import secrets
import time
import warnings
from collections import defaultdict
from datetime import datetime, timedelta
from threading import Lock

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
import models

# ── JWT secret ────────────────────────────────────────────────────────────────
# MUST be set via the SECRET_KEY environment variable in production.
# A random fallback is generated per-process start so that omitting the variable
# is safe for development but immediately obvious (sessions reset on restart).
SECRET_KEY: str = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(32)
    warnings.warn(
        "[LMS] SECRET_KEY is not set. A random key was generated — all "
        "sessions will be lost on restart. Set SECRET_KEY in production.",
        stacklevel=1,
    )

ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

# ── bcrypt context ────────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# A pre-hashed dummy value used so that failed logins for unknown emails still
# run the full bcrypt verification, preventing timing-based user enumeration.
DUMMY_HASH: str = pwd_context.hash("__lms_dummy_prevent_timing_attack__")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ── Password policy ───────────────────────────────────────────────────────────
_MIN_PW_LEN = 8
_MAX_PW_LEN = 128


def validate_password(password: str) -> str:
    """
    Enforce password strength.  Raises ValueError on failure so it integrates
    cleanly with Pydantic field_validators (returns 422 to the caller).
    """
    if len(password) < _MIN_PW_LEN:
        raise ValueError(f"Password must be at least {_MIN_PW_LEN} characters long")
    if len(password) > _MAX_PW_LEN:
        raise ValueError(f"Password must not exceed {_MAX_PW_LEN} characters")
    if not any(c.isalpha() for c in password):
        raise ValueError("Password must contain at least one letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit")
    return password


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ── JWT utilities ─────────────────────────────────────────────────────────────
def create_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise err
    except JWTError:
        raise err
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise err
    return user


def require_role(*roles):
    def checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return checker


# ── Course-ownership guard ────────────────────────────────────────────────────
def require_course_access(course_id: int, current_user: models.User, db: Session) -> models.Course:
    """
    Return the course if the caller is an admin or the course's own teacher.
    Raises 404 if the course doesn't exist, 403 if access is denied.
    Used in material/assignment/quiz/session routes to enforce ownership.
    """
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    if current_user.role == "admin":
        return course
    if current_user.role == "teacher" and course.teacher_id == current_user.id:
        return course
    raise HTTPException(403, "You don't have permission to manage this course")


# ── Rate limiter ──────────────────────────────────────────────────────────────
class _RateLimiter:
    """
    Thread-safe sliding-window in-memory rate limiter.
    Automatically bypassed when the TESTING environment variable is set
    so that the test suite never hits rate limits.
    """

    def __init__(self, max_calls: int, window_seconds: int):
        self._max = max_calls
        self._window = window_seconds
        self._store: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    def is_allowed(self, key: str) -> bool:
        if os.getenv("TESTING"):
            return True  # no limits in test environment
        now = time.time()
        cutoff = now - self._window
        with self._lock:
            self._store[key] = [t for t in self._store[key] if t > cutoff]
            if len(self._store[key]) >= self._max:
                return False
            self._store[key].append(now)
            return True


# 10 login attempts per IP per 60 seconds
login_limiter = _RateLimiter(max_calls=10, window_seconds=60)
