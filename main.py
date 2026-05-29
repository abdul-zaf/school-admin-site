import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

from database import Base, engine, SessionLocal
import models
import security
from routers import auth, users, courses, assignments, announcements, sessions, quizzes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="School LMS", docs_url="/api/docs")

# ── CORS ───────────────────────────────────────────────────────────────────────
# In production set ALLOWED_ORIGINS=https://yourdomain.com (comma-separated).
_allowed_origins = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# ── Security headers ───────────────────────────────────────────────────────────
class _SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        response = await call_next(request)
        h = response.headers
        h["X-Content-Type-Options"]  = "nosniff"
        h["X-Frame-Options"]         = "DENY"
        h["X-XSS-Protection"]        = "1; mode=block"
        h["Referrer-Policy"]         = "strict-origin-when-cross-origin"
        h["Permissions-Policy"]      = "geolocation=(), microphone=(), camera=()"
        # Only add HSTS once TLS is in front of the app
        if os.getenv("ENVIRONMENT") == "production":
            h["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


app.add_middleware(_SecurityHeadersMiddleware)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(auth.router,          prefix="/api/auth",          tags=["auth"])
app.include_router(users.router,         prefix="/api/users",         tags=["users"])
app.include_router(courses.router,       prefix="/api/courses",       tags=["courses"])
app.include_router(assignments.router,   prefix="/api/assignments",   tags=["assignments"])
app.include_router(announcements.router, prefix="/api/announcements", tags=["announcements"])
app.include_router(sessions.router,      prefix="/api/sessions",      tags=["sessions"])
app.include_router(quizzes.router,       prefix="/api/quizzes",       tags=["quizzes"])

app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Seed ───────────────────────────────────────────────────────────────────────
def seed_admin():
    db = SessionLocal()
    try:
        if not db.query(models.User).filter(models.User.email == "admin@school.edu").first():
            db.add(models.User(
                name="Administrator",
                email="admin@school.edu",
                password_hash=security.hash_password("Admin123"),  # meets policy
                role="admin",
            ))
            db.commit()
    finally:
        db.close()


if not os.getenv("TESTING"):
    seed_admin()


@app.get("/")
def root():
    return FileResponse("static/index.html")
