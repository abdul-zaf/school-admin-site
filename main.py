import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import Base, engine, SessionLocal
import models
import security
from routers import auth, users, courses, assignments, announcements, sessions, quizzes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="School LMS", docs_url="/api/docs")

app.include_router(auth.router,          prefix="/api/auth",          tags=["auth"])
app.include_router(users.router,         prefix="/api/users",         tags=["users"])
app.include_router(courses.router,       prefix="/api/courses",       tags=["courses"])
app.include_router(assignments.router,   prefix="/api/assignments",   tags=["assignments"])
app.include_router(announcements.router, prefix="/api/announcements", tags=["announcements"])
app.include_router(sessions.router,      prefix="/api/sessions",      tags=["sessions"])
app.include_router(quizzes.router,       prefix="/api/quizzes",       tags=["quizzes"])

app.mount("/static", StaticFiles(directory="static"), name="static")


def seed_admin():
    db = SessionLocal()
    try:
        if not db.query(models.User).filter(models.User.email == "admin@school.edu").first():
            db.add(models.User(
                name="Administrator",
                email="admin@school.edu",
                password_hash=security.hash_password("admin123"),
                role="admin",
            ))
            db.commit()
    finally:
        db.close()


# Skip automatic seeding when running under pytest (fixtures handle test data)
if not os.getenv("TESTING"):
    seed_admin()


@app.get("/")
def root():
    return FileResponse("static/index.html")
