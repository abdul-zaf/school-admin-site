def test_create_course_as_admin(client, admin_h):
    r = client.post("/api/courses/", json={"title": "Biology", "subject": "Science"}, headers=admin_h)
    assert r.status_code == 200
    assert r.json()["title"] == "Biology"


def test_create_course_as_teacher(client, teacher_h):
    r = client.post("/api/courses/", json={"title": "Art"}, headers=teacher_h)
    assert r.status_code == 200


def test_create_course_forbidden_for_student(client, student_h):
    r = client.post("/api/courses/", json={"title": "X"}, headers=student_h)
    assert r.status_code == 403


def test_list_courses(client, admin_h, course_id):
    r = client.get("/api/courses/", headers=admin_h)
    assert r.status_code == 200
    ids = [c["id"] for c in r.json()]
    assert course_id in ids


def test_get_course_detail(client, admin_h, course_id):
    r = client.get(f"/api/courses/{course_id}", headers=admin_h)
    assert r.status_code == 200
    assert r.json()["id"] == course_id


def test_update_course(client, admin_h, course_id):
    r = client.put(f"/api/courses/{course_id}",
                   json={"title": "Updated", "subject": "New"}, headers=admin_h)
    assert r.status_code == 200


def test_delete_course(client, admin_h):
    cid = client.post("/api/courses/", json={"title": "Temp"}, headers=admin_h).json()["id"]
    r = client.delete(f"/api/courses/{cid}", headers=admin_h)
    assert r.status_code == 200


# ── Enrollment ─────────────────────────────────────────────────────────────

def test_student_can_enroll(client, student_h, course_id):
    r = client.post(f"/api/courses/{course_id}/enroll", headers=student_h)
    assert r.status_code == 200


def test_student_cannot_enroll_twice(client, student_h, course_id):
    client.post(f"/api/courses/{course_id}/enroll", headers=student_h)
    r = client.post(f"/api/courses/{course_id}/enroll", headers=student_h)
    assert r.status_code == 400


def test_student_can_unenroll(client, student_h, course_id):
    client.post(f"/api/courses/{course_id}/enroll", headers=student_h)
    r = client.delete(f"/api/courses/{course_id}/enroll", headers=student_h)
    assert r.status_code == 200


def test_enrolled_flag_in_list(client, student_h, course_id):
    client.post(f"/api/courses/{course_id}/enroll", headers=student_h)
    courses = client.get("/api/courses/", headers=student_h).json()
    match = next((c for c in courses if c["id"] == course_id), None)
    assert match and match["enrolled"] is True


# ── Materials ──────────────────────────────────────────────────────────────

def test_add_and_list_material(client, admin_h, course_id):
    r = client.post(f"/api/courses/{course_id}/materials",
                    json={"title": "Handout", "content": "Notes here"}, headers=admin_h)
    assert r.status_code == 200
    mats = client.get(f"/api/courses/{course_id}/materials", headers=admin_h).json()
    assert any(m["title"] == "Handout" for m in mats)


def test_delete_material(client, admin_h, course_id):
    mid = client.post(f"/api/courses/{course_id}/materials",
                      json={"title": "Del"}, headers=admin_h).json()["id"]
    r = client.delete(f"/api/courses/{course_id}/materials/{mid}", headers=admin_h)
    assert r.status_code == 200


# ── Students sub-resource ──────────────────────────────────────────────────

def test_list_students_admin_sees_enrolled(client, admin_h, student_h, course_id):
    client.post(f"/api/courses/{course_id}/enroll", headers=student_h)
    r = client.get(f"/api/courses/{course_id}/students", headers=admin_h)
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["email"] == "student@test.com"


def test_list_students_own_teacher_allowed(client, teacher_h, student_h, course_id):
    # course_id is owned by admin; create a course owned by teacher
    cid = client.post("/api/courses/", json={"title": "Teacher Course"}, headers=teacher_h).json()["id"]
    client.post(f"/api/courses/{cid}/enroll", headers=student_h)
    r = client.get(f"/api/courses/{cid}/students", headers=teacher_h)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_list_students_other_teacher_forbidden(client, teacher_h, course_id):
    # course_id belongs to admin, not teacher
    r = client.get(f"/api/courses/{course_id}/students", headers=teacher_h)
    assert r.status_code == 403


def test_list_students_student_forbidden(client, student_h, course_id):
    r = client.get(f"/api/courses/{course_id}/students", headers=student_h)
    assert r.status_code == 403


def test_list_students_empty_before_enrollment(client, admin_h, course_id):
    r = client.get(f"/api/courses/{course_id}/students", headers=admin_h)
    assert r.status_code == 200
    assert r.json() == []
