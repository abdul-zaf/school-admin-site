import pytest


@pytest.fixture
def assignment_id(client, admin_h, course_id):
    r = client.post(f"/api/assignments/course/{course_id}", json={
        "title": "Homework 1", "description": "Do the thing.", "max_score": 50.0,
    }, headers=admin_h)
    assert r.status_code == 200
    return r.json()["id"]


def test_create_assignment(client, admin_h, course_id):
    r = client.post(f"/api/assignments/course/{course_id}",
                    json={"title": "Essay", "max_score": 100.0}, headers=admin_h)
    assert r.status_code == 200
    assert r.json()["title"] == "Essay"


def test_list_assignments(client, admin_h, assignment_id, course_id):
    r = client.get(f"/api/assignments/course/{course_id}", headers=admin_h)
    assert r.status_code == 200
    ids = [a["id"] for a in r.json()]
    assert assignment_id in ids


def test_get_assignment_detail(client, admin_h, assignment_id):
    r = client.get(f"/api/assignments/{assignment_id}", headers=admin_h)
    assert r.status_code == 200
    assert r.json()["id"] == assignment_id


def test_student_submit_assignment(client, student_h, assignment_id):
    r = client.post(f"/api/assignments/{assignment_id}/submit",
                    json={"content": "My answer."}, headers=student_h)
    assert r.status_code == 200


def test_student_resubmit_assignment(client, student_h, assignment_id):
    client.post(f"/api/assignments/{assignment_id}/submit",
                json={"content": "First."}, headers=student_h)
    r = client.post(f"/api/assignments/{assignment_id}/submit",
                    json={"content": "Updated."}, headers=student_h)
    assert r.status_code == 200
    assert r.json().get("resubmitted") is True


def test_teacher_grades_submission(client, admin_h, student_h, assignment_id):
    # Student submits first
    client.post(f"/api/assignments/{assignment_id}/submit",
                json={"content": "Answer."}, headers=student_h)
    # Teacher fetches submission list
    detail = client.get(f"/api/assignments/{assignment_id}", headers=admin_h).json()
    assert len(detail["submissions"]) == 1
    sub_id = detail["submissions"][0]["id"]
    # Grade it
    r = client.put(f"/api/assignments/submissions/{sub_id}/grade",
                   json={"score": 45.0, "feedback": "Good work!"}, headers=admin_h)
    assert r.status_code == 200
    # Confirm grade stored
    detail2 = client.get(f"/api/assignments/{assignment_id}", headers=admin_h).json()
    assert detail2["submissions"][0]["score"] == 45.0


def test_delete_assignment(client, admin_h, assignment_id):
    r = client.delete(f"/api/assignments/{assignment_id}", headers=admin_h)
    assert r.status_code == 200
