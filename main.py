import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

from database import Base, engine, SessionLocal, apply_migrations
import models
import security
from routers import (
    auth, users, courses, assignments, announcements, sessions, quizzes,
    discussions, messages, notifications, gradebook, rubrics, question_banks,
    modules, analytics, badges, parents, surveys, portfolio,
    # ── New: Learning Intelligence & Social ──────────────────────────────────
    spaced_repetition, teach_back, confusion, help_board, knowledge_graph,
    study_groups,
    # ── Auth extras ──────────────────────────────────────────────────────────
    password_reset,
)

Base.metadata.create_all(bind=engine)
apply_migrations()   # safe no-op if columns already exist

app = FastAPI(title="School LMS", docs_url="/api/docs")

# ── CORS ───────────────────────────────────────────────────────────────────────
# Priority order:
#   1. ALLOWED_ORIGINS env var  (explicit, comma-separated list)
#   2. RENDER_EXTERNAL_URL      (Render injects this automatically — no config needed)
#   3. localhost fallback       (local dev)
_render_url   = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
_default_cors = f"http://localhost:8000,{_render_url}" if _render_url else "http://localhost:8000"
_allowed_origins = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", _default_cors).split(",")
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
app.include_router(auth.router,           prefix="/api/auth",           tags=["auth"])
app.include_router(password_reset.router, prefix="/api/auth",           tags=["auth"])
app.include_router(users.router,          prefix="/api/users",          tags=["users"])
app.include_router(courses.router,        prefix="/api/courses",        tags=["courses"])
app.include_router(assignments.router,    prefix="/api/assignments",    tags=["assignments"])
app.include_router(announcements.router,  prefix="/api/announcements",  tags=["announcements"])
app.include_router(sessions.router,       prefix="/api/sessions",       tags=["sessions"])
app.include_router(quizzes.router,        prefix="/api/quizzes",        tags=["quizzes"])
app.include_router(discussions.router,    prefix="/api/discussions",    tags=["discussions"])
app.include_router(messages.router,       prefix="/api/messages",       tags=["messages"])
app.include_router(notifications.router,  prefix="/api/notifications",  tags=["notifications"])
app.include_router(gradebook.router,      prefix="/api/gradebook",      tags=["gradebook"])
app.include_router(rubrics.router,        prefix="/api/rubrics",        tags=["rubrics"])
app.include_router(question_banks.router, prefix="/api/question-banks", tags=["question-banks"])
app.include_router(modules.router,        prefix="/api/modules",        tags=["modules"])
app.include_router(analytics.router,      prefix="/api/analytics",      tags=["analytics"])
app.include_router(badges.router,         prefix="/api/badges",         tags=["badges"])
app.include_router(parents.router,        prefix="/api/parents",        tags=["parents"])
app.include_router(surveys.router,        prefix="/api/surveys",        tags=["surveys"])
app.include_router(portfolio.router,      prefix="/api/portfolio",      tags=["portfolio"])
# ── Learning Intelligence & Social ─────────────────────────────────────────
app.include_router(spaced_repetition.router, prefix="/api/sr",             tags=["spaced-repetition"])
app.include_router(teach_back.router,        prefix="/api/teach-back",     tags=["teach-back"])
app.include_router(confusion.router,         prefix="/api/confusion",      tags=["confusion"])
app.include_router(help_board.router,        prefix="/api/help",           tags=["help-board"])
app.include_router(knowledge_graph.router,   prefix="/api/graph",          tags=["knowledge-graph"])
app.include_router(study_groups.router,      prefix="/api/study-groups",   tags=["study-groups"])

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


# ── External integration stubs ─────────────────────────────────────────────────
# The following integrations require external services and are intentionally
# left as stubs. Implement by registering dedicated routers below.

# SCORM / LTI — uncomment and implement routers/scorm.py + routers/lti.py
# app.include_router(scorm.router, prefix="/api/scorm", tags=["scorm"])
# app.include_router(lti.router,   prefix="/api/lti",   tags=["lti"])

# Turnitin plagiarism detection — requires Turnitin API credentials
# app.include_router(turnitin.router, prefix="/api/turnitin", tags=["turnitin"])

# SSO / LDAP — implement via python-ldap or authlib (SAML/OAuth2)
# app.include_router(sso.router, prefix="/api/sso", tags=["sso"])

# Live video (Zoom/Google Meet/BigBlueButton) — requires vendor SDK
# app.include_router(video.router, prefix="/api/video", tags=["video"])

# AI Proctoring — requires computer vision service integration
# app.include_router(proctoring.router, prefix="/api/proctoring", tags=["proctoring"])
