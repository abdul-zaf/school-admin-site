def test_list_users_as_admin(client, admin_h):
    r = client.get("/api/users/", headers=admin_h)
    assert r.status_code == 200
    emails = [u["email"] for u in r.json()]
    assert "admin@test.com" in emails
    assert "teacher@test.com" in emails
    assert "student@test.com" in emails


def test_list_users_forbidden_for_student(client, student_h):
    r = client.get("/api/users/", headers=student_h)
    assert r.status_code == 403


def test_list_users_forbidden_for_teacher(client, teacher_h):
    r = client.get("/api/users/", headers=teacher_h)
    assert r.status_code == 403


def test_create_user(client, admin_h):
    r = client.post("/api/users/", json={
        "name": "New Student", "email": "new@test.com",
        "password": "Pass1234", "role": "student",
    }, headers=admin_h)
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == "new@test.com"
    assert body["role"] == "student"


def test_create_user_duplicate_email(client, admin_h):
    # Names must be >= 2 chars per the name policy
    client.post("/api/users/", json={
        "name": "Alice", "email": "dup@test.com", "password": "Pass1234",
    }, headers=admin_h)
    r = client.post("/api/users/", json={
        "name": "Bob", "email": "dup@test.com", "password": "Pass1234",
    }, headers=admin_h)
    assert r.status_code == 400


def test_delete_user(client, admin_h):
    uid = client.post("/api/users/", json={
        "name": "Temp", "email": "temp@test.com", "password": "Pass1234",
    }, headers=admin_h).json()["id"]
    r = client.delete(f"/api/users/{uid}", headers=admin_h)
    assert r.status_code == 200


def test_cannot_delete_self(client, admin_h):
    me = client.get("/api/users/me", headers=admin_h).json()
    r = client.delete(f"/api/users/{me['id']}", headers=admin_h)
    assert r.status_code == 400


def test_filter_users_by_role(client, admin_h):
    r = client.get("/api/users/?role=teacher", headers=admin_h)
    assert r.status_code == 200
    assert all(u["role"] == "teacher" for u in r.json())
