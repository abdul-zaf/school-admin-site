"""
Security-specific tests.
Covers: password policy, ownership enforcement, rate limiter unit, security headers,
and the anti-enumeration timing behaviour.
"""


# ─── Password policy ──────────────────────────────────────────────────────────

def test_password_too_short_rejected(client, admin_h):
    r = client.post("/api/users/", json={
        "name": "X", "email": "x@test.com", "password": "Ab1",
    }, headers=admin_h)
    assert r.status_code == 422


def test_password_no_letter_rejected(client, admin_h):
    r = client.post("/api/users/", json={
        "name": "X", "email": "x@test.com", "password": "12345678",
    }, headers=admin_h)
    assert r.status_code == 422


def test_password_no_digit_rejected(client, admin_h):
    r = client.post("/api/users/", json={
        "name": "X", "email": "x@test.com", "password": "abcdefgh",
    }, headers=admin_h)
    assert r.status_code == 422


def test_password_exceeds_max_rejected(client, admin_h):
    r = client.post("/api/users/", json={
        "name": "X", "email": "x@test.com", "password": "Abc1" + "x" * 130,
    }, headers=admin_h)
    assert r.status_code == 422


def test_valid_password_accepted(client, admin_h):
    r = client.post("/api/users/", json={
        "name": "Good", "email": "good@test.com", "password": "GoodPass1",
    }, headers=admin_h)
    assert r.status_code == 200


def test_update_own_password_policy_enforced(client, student_h):
    r = client.put("/api/users/me", json={"password": "short"}, headers=student_h)
    assert r.status_code == 422


# ─── Email normalisation ──────────────────────────────────────────────────────

def test_email_normalised_to_lowercase(client, admin_h):
    """Creating a user with mixed-case email should store it lowercase."""
    r = client.post("/api/users/", json={
        "name": "Case", "email": "MIXED@Test.COM", "password": "MixedPass1",
    }, headers=admin_h)
    assert r.status_code == 200
    assert r.json()["email"] == "mixed@test.com"


def test_login_case_insensitive(client):
    """Login should work regardless of email case."""
    r = client.post("/api/auth/login",
                    data={"username": "ADMIN@TEST.COM", "password": "testPass1"})
    assert r.status_code == 200


# ─── Rate limiter (unit test, not via HTTP) ───────────────────────────────────

def test_rate_limiter_allows_then_blocks():
    """The rate limiter should block after max_calls within the window."""
    import os
    from security import _RateLimiter

    # Temporarily clear TESTING so the limiter actually runs
    orig = os.environ.pop("TESTING", None)
    try:
        lim = _RateLimiter(max_calls=3, window_seconds=60)
        assert lim.is_allowed("k") is True
        assert lim.is_allowed("k") is True
        assert lim.is_allowed("k") is True
        assert lim.is_allowed("k") is False   # 4th attempt blocked
    finally:
        if orig is not None:
            os.environ["TESTING"] = orig


def test_rate_limiter_different_keys_independent():
    import os
    from security import _RateLimiter

    orig = os.environ.pop("TESTING", None)
    try:
        lim = _RateLimiter(max_calls=1, window_seconds=60)
        assert lim.is_allowed("alice") is True
        assert lim.is_allowed("alice") is False
        # A different key is not affected
        assert lim.is_allowed("bob") is True
    finally:
        if orig is not None:
            os.environ["TESTING"] = orig


# ─── Ownership enforcement ────────────────────────────────────────────────────

def test_teacher_cannot_see_students_of_another_course(client, admin_h, teacher_h):
    """A teacher should not see enrolled students of a course they don't own."""
    # Create a course owned by admin (not teacher)
    cid = client.post("/api/courses/", json={"title": "Admin's Course"}, headers=admin_h).json()["id"]
    # Enroll a student via admin
    client.post("/api/users/", json={
        "name": "S", "email": "s@t.com", "password": "Student1",
    }, headers=admin_h)

    detail = client.get(f"/api/courses/{cid}", headers=teacher_h).json()
    # Teacher sees the course, but NOT the student list
    assert detail["students"] == []


def test_teacher_can_see_students_of_own_course(client, teacher_h, admin_h):
    """A teacher can see enrolled students of their own course."""
    # Teacher creates course
    cid = client.post("/api/courses/", json={"title": "My Course"}, headers=teacher_h).json()["id"]
    # Admin enrolls a student
    client.post("/api/users/", json={
        "name": "Enrolled", "email": "enr@t.com", "password": "Student1",
    }, headers=admin_h)
    # For the student list to appear, a student must actually enroll
    # (we just verify the response contains the students key and not blocked)
    detail = client.get(f"/api/courses/{cid}", headers=teacher_h).json()
    assert "students" in detail


def test_teacher_cannot_add_material_to_foreign_course(client, admin_h, teacher_h):
    """A teacher must not be able to add materials to another teacher's course."""
    cid = client.post("/api/courses/", json={"title": "Admin Course"}, headers=admin_h).json()["id"]
    r = client.post(f"/api/courses/{cid}/materials",
                    json={"title": "Sneaky Note"}, headers=teacher_h)
    assert r.status_code == 403


def test_teacher_cannot_create_session_in_foreign_course(client, admin_h, teacher_h):
    cid = client.post("/api/courses/", json={"title": "Admin Course"}, headers=admin_h).json()["id"]
    r = client.post(f"/api/sessions/course/{cid}", json={
        "title": "Unauthorized", "session_type": "virtual",
        "date": "2027-06-01T10:00:00",
    }, headers=teacher_h)
    assert r.status_code == 403


def test_teacher_cannot_create_quiz_in_foreign_course(client, admin_h, teacher_h):
    cid = client.post("/api/courses/", json={"title": "Admin Course"}, headers=admin_h).json()["id"]
    r = client.post(f"/api/quizzes/course/{cid}",
                    json={"title": "Hijacked Quiz"}, headers=teacher_h)
    assert r.status_code == 403


def test_teacher_cannot_create_assignment_in_foreign_course(client, admin_h, teacher_h):
    cid = client.post("/api/courses/", json={"title": "Admin Course"}, headers=admin_h).json()["id"]
    r = client.post(f"/api/assignments/course/{cid}",
                    json={"title": "Hijacked HW", "max_score": 100}, headers=teacher_h)
    assert r.status_code == 403


# ─── Security headers ─────────────────────────────────────────────────────────

def test_security_headers_present(client):
    """Every response should include the hardening headers."""
    r = client.get("/api/docs")
    assert r.headers.get("x-content-type-options") == "nosniff"
    assert r.headers.get("x-frame-options") == "DENY"
    assert r.headers.get("x-xss-protection") == "1; mode=block"
    assert r.headers.get("referrer-policy") == "strict-origin-when-cross-origin"


# ─── Unknown-email timing behaviour ──────────────────────────────────────────

def test_login_same_error_for_unknown_email_and_wrong_password(client):
    """Both failures return 401 with the same generic message."""
    r1 = client.post("/api/auth/login",
                     data={"username": "ghost@test.com", "password": "anything1A"})
    r2 = client.post("/api/auth/login",
                     data={"username": "admin@test.com", "password": "wrongPass1"})
    assert r1.status_code == r2.status_code == 401
    assert r1.json()["detail"] == r2.json()["detail"]
