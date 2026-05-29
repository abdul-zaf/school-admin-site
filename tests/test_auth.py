def test_login_success(client):
    r = client.post("/api/auth/login", data={"username": "admin@test.com", "password": "testpass"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["role"] == "admin"
    assert data["name"] == "Admin"


def test_login_wrong_password(client):
    r = client.post("/api/auth/login", data={"username": "admin@test.com", "password": "badpass"})
    assert r.status_code == 401


def test_login_unknown_email(client):
    r = client.post("/api/auth/login", data={"username": "nobody@test.com", "password": "testpass"})
    assert r.status_code == 401


def test_get_me_authenticated(client, admin_h):
    r = client.get("/api/users/me", headers=admin_h)
    assert r.status_code == 200
    assert r.json()["email"] == "admin@test.com"
    assert r.json()["role"] == "admin"


def test_get_me_unauthenticated(client):
    r = client.get("/api/users/me")
    assert r.status_code == 401


def test_get_me_bad_token(client):
    r = client.get("/api/users/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert r.status_code == 401


def test_update_own_name(client, admin_h):
    r = client.put("/api/users/me", json={"name": "Updated Admin"}, headers=admin_h)
    assert r.status_code == 200
    assert r.json()["name"] == "Updated Admin"
