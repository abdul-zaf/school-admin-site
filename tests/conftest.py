"""
Shared pytest fixtures.

Environment variables must be set BEFORE any application module is imported
so that SQLAlchemy's engine points at the test database.
"""
import os
import pathlib

# ── Must be first ─────────────────────────────────────────────────────────────
os.environ["TESTING"]      = "1"                         # suppresses seed_admin()
os.environ["DATABASE_URL"] = "sqlite:///./test_lms.db"  # isolated test DB

# Remove any leftover DB file from a previous aborted run.
# On Windows a previous pytest process may still hold the file open; the
# per-test clean_db fixture (drop_all / create_all) will reset state anyway,
# so a PermissionError here is safe to ignore.
_test_db = pathlib.Path("test_lms.db")
if _test_db.exists():
    try:
        _test_db.unlink()
    except PermissionError:
        pass  # file still in use; clean_db fixture will reset the schema

# ── App imports (after env vars are set) ──────────────────────────────────────
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from database import Base, engine  # noqa: E402
from main import app  # noqa: E402  ← triggers create_all on test DB (no seed_admin)
import models   # noqa: E402
import security  # noqa: E402

# Flush any connections left open by main.py's create_all + apply_migrations.
# This prevents stale pooled connections from carrying dirty SQLite state into
# the clean_db fixture's drop_all / create_all cycle.
engine.dispose()

_Session = sessionmaker(bind=engine)


# ── Helpers ───────────────────────────────────────────────────────────────────
def _add_user(name, email, role):
    db = _Session()
    u = models.User(
        name=name,
        email=email,
        password_hash=security.hash_password("testPass1"),
        role=role,
    )
    db.add(u)
    db.commit()
    db.close()


# ── Per-test DB reset ─────────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def clean_db():
    """Drop and recreate every table before each test for full isolation."""
    # Dispose before drop so no pooled connection carries a stale schema view.
    engine.dispose()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    _add_user("Admin",   "admin@test.com",   "admin")
    _add_user("Teacher", "teacher@test.com", "teacher")
    _add_user("Student", "student@test.com", "student")
    yield
    # Dispose again so the next test's drop_all doesn't inherit open connections.
    engine.dispose()
    Base.metadata.drop_all(bind=engine)


# ── Client fixture ────────────────────────────────────────────────────────────
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


# ── Auth helpers ──────────────────────────────────────────────────────────────
def _login(client, email):
    r = client.post(
        "/api/auth/login",
        data={"username": email, "password": "testPass1"},
    )
    assert r.status_code == 200, f"Login failed for {email}: {r.text}"
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture
def admin_h(client):
    return _login(client, "admin@test.com")


@pytest.fixture
def teacher_h(client):
    return _login(client, "teacher@test.com")


@pytest.fixture
def student_h(client):
    return _login(client, "student@test.com")


# ── Shared data fixtures ──────────────────────────────────────────────────────
@pytest.fixture
def course_id(client, admin_h):
    """A course owned by the admin, ready for use in tests."""
    r = client.post(
        "/api/courses/",
        json={"title": "Test Course", "subject": "Testing"},
        headers=admin_h,
    )
    assert r.status_code == 200, r.text
    return r.json()["id"]
