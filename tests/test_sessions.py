import pytest

SESSION_DATE = "2027-06-01T10:00:00"


def test_create_virtual_session(client, teacher_h):
    # Teacher creates their own course first, then adds a session
    cid = client.post("/api/courses/", json={"title": "Teacher Course"}, headers=teacher_h).json()["id"]
    r = client.post(f"/api/sessions/course/{cid}", json={
        "title": "Online Class",
        "session_type": "virtual",
        "date": SESSION_DATE,
        "duration_minutes": 60,
        "location": "https://meet.google.com/abc-defg-hij",
    }, headers=teacher_h)
    assert r.status_code == 200
    assert r.json()["title"] == "Online Class"


def test_create_physical_session(client, admin_h, course_id):
    r = client.post(f"/api/sessions/course/{course_id}", json={
        "title": "Classroom Lecture",
        "session_type": "physical",
        "date": SESSION_DATE,
        "duration_minutes": 90,
        "location": "Room 204, Block B",
    }, headers=admin_h)
    assert r.status_code == 200


def test_invalid_session_type_rejected(client, admin_h, course_id):
    r = client.post(f"/api/sessions/course/{course_id}", json={
        "title": "Bad",
        "session_type": "hybrid",
        "date": SESSION_DATE,
    }, headers=admin_h)
    assert r.status_code == 400


def test_list_sessions(client, admin_h, course_id):
    client.post(f"/api/sessions/course/{course_id}", json={
        "title": "S1", "session_type": "virtual", "date": SESSION_DATE,
    }, headers=admin_h)
    r = client.get(f"/api/sessions/course/{course_id}", headers=admin_h)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_student_can_view_sessions(client, student_h, admin_h, course_id):
    client.post(f"/api/sessions/course/{course_id}", json={
        "title": "Public Session", "session_type": "physical", "date": SESSION_DATE,
    }, headers=admin_h)
    r = client.get(f"/api/sessions/course/{course_id}", headers=student_h)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_student_cannot_create_session(client, student_h, course_id):
    r = client.post(f"/api/sessions/course/{course_id}", json={
        "title": "Nope", "session_type": "virtual", "date": SESSION_DATE,
    }, headers=student_h)
    assert r.status_code == 403


def test_delete_session(client, admin_h, course_id):
    sid = client.post(f"/api/sessions/course/{course_id}", json={
        "title": "Temp", "session_type": "virtual", "date": SESSION_DATE,
    }, headers=admin_h).json()["id"]
    r = client.delete(f"/api/sessions/{sid}", headers=admin_h)
    assert r.status_code == 200
