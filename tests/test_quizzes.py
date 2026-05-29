import pytest


@pytest.fixture
def quiz_id(client, admin_h, course_id):
    r = client.post(f"/api/quizzes/course/{course_id}",
                    json={"title": "Chapter 1 Quiz", "time_limit": 30}, headers=admin_h)
    assert r.status_code == 200
    return r.json()["id"]


@pytest.fixture
def mc_question_id(client, admin_h, quiz_id):
    r = client.post(f"/api/quizzes/{quiz_id}/questions", json={
        "question_text": "What is 2 + 2?",
        "question_type": "multiple_choice",
        "points": 2.0,
        "options": [
            {"option_text": "3", "is_correct": False},
            {"option_text": "4", "is_correct": True},
            {"option_text": "5", "is_correct": False},
        ],
    }, headers=admin_h)
    assert r.status_code == 200
    return r.json()["id"]


def test_create_quiz(client, admin_h, course_id):
    r = client.post(f"/api/quizzes/course/{course_id}",
                    json={"title": "Pop Quiz"}, headers=admin_h)
    assert r.status_code == 200
    assert r.json()["title"] == "Pop Quiz"


def test_list_quizzes(client, admin_h, quiz_id, course_id):
    r = client.get(f"/api/quizzes/course/{course_id}", headers=admin_h)
    assert r.status_code == 200
    assert any(q["id"] == quiz_id for q in r.json())


def test_add_multiple_choice_question(client, admin_h, quiz_id):
    r = client.post(f"/api/quizzes/{quiz_id}/questions", json={
        "question_text": "Colour of the sky?",
        "question_type": "multiple_choice",
        "points": 1.0,
        "options": [
            {"option_text": "Blue",  "is_correct": True},
            {"option_text": "Green", "is_correct": False},
        ],
    }, headers=admin_h)
    assert r.status_code == 200


def test_add_true_false_question(client, admin_h, quiz_id):
    r = client.post(f"/api/quizzes/{quiz_id}/questions", json={
        "question_text": "The earth is flat.",
        "question_type": "true_false",
        "points": 1.0,
        "options": [
            {"option_text": "True",  "is_correct": False},
            {"option_text": "False", "is_correct": True},
        ],
    }, headers=admin_h)
    assert r.status_code == 200


def test_add_short_answer_question(client, admin_h, quiz_id):
    r = client.post(f"/api/quizzes/{quiz_id}/questions", json={
        "question_text": "Explain photosynthesis.",
        "question_type": "short_answer",
        "points": 5.0,
        "options": [],
    }, headers=admin_h)
    assert r.status_code == 200


def test_get_quiz_hides_correct_answers_from_student(client, student_h, quiz_id, mc_question_id):
    r = client.get(f"/api/quizzes/{quiz_id}", headers=student_h)
    assert r.status_code == 200
    for q in r.json()["questions"]:
        for opt in q["options"]:
            assert "is_correct" not in opt


def test_get_quiz_shows_correct_answers_to_teacher(client, admin_h, quiz_id, mc_question_id):
    r = client.get(f"/api/quizzes/{quiz_id}", headers=admin_h)
    assert r.status_code == 200
    for q in r.json()["questions"]:
        for opt in q["options"]:
            assert "is_correct" in opt


def test_student_starts_quiz(client, student_h, quiz_id, mc_question_id):
    r = client.post(f"/api/quizzes/{quiz_id}/start", headers=student_h)
    assert r.status_code == 200
    assert "attempt_id" in r.json()


def test_student_cannot_start_twice(client, student_h, quiz_id, mc_question_id):
    client.post(f"/api/quizzes/{quiz_id}/start", headers=student_h)
    # Starting again should return the existing attempt (not 400)
    r = client.post(f"/api/quizzes/{quiz_id}/start", headers=student_h)
    assert r.status_code == 200


def test_auto_grade_mc_quiz(client, admin_h, student_h, quiz_id, mc_question_id):
    # Get the quiz to find option IDs
    quiz = client.get(f"/api/quizzes/{quiz_id}", headers=admin_h).json()
    q = quiz["questions"][0]
    correct_opt = next(o for o in q["options"] if o["is_correct"])

    # Start + submit with correct answer
    client.post(f"/api/quizzes/{quiz_id}/start", headers=student_h)
    r = client.post(f"/api/quizzes/{quiz_id}/submit", json={
        "answers": [{"question_id": q["id"], "selected_option_id": correct_opt["id"]}]
    }, headers=student_h)
    assert r.status_code == 200
    body = r.json()
    assert body["score"] == q["points"]
    assert body["has_short_answer"] is False


def test_wrong_answer_scores_zero(client, admin_h, student_h, quiz_id, mc_question_id):
    quiz = client.get(f"/api/quizzes/{quiz_id}", headers=admin_h).json()
    q = quiz["questions"][0]
    wrong_opt = next(o for o in q["options"] if not o["is_correct"])

    client.post(f"/api/quizzes/{quiz_id}/start", headers=student_h)
    r = client.post(f"/api/quizzes/{quiz_id}/submit", json={
        "answers": [{"question_id": q["id"], "selected_option_id": wrong_opt["id"]}]
    }, headers=student_h)
    assert r.status_code == 200
    assert r.json()["score"] == 0.0


def test_delete_question(client, admin_h, quiz_id, mc_question_id):
    r = client.delete(f"/api/quizzes/questions/{mc_question_id}", headers=admin_h)
    assert r.status_code == 200


def test_delete_quiz(client, admin_h, quiz_id):
    r = client.delete(f"/api/quizzes/{quiz_id}", headers=admin_h)
    assert r.status_code == 200


def test_teacher_views_attempts(client, admin_h, student_h, quiz_id, mc_question_id):
    quiz = client.get(f"/api/quizzes/{quiz_id}", headers=admin_h).json()
    q = quiz["questions"][0]
    opt_id = q["options"][0]["id"]
    client.post(f"/api/quizzes/{quiz_id}/start", headers=student_h)
    client.post(f"/api/quizzes/{quiz_id}/submit", json={
        "answers": [{"question_id": q["id"], "selected_option_id": opt_id}]
    }, headers=student_h)

    r = client.get(f"/api/quizzes/{quiz_id}/attempts", headers=admin_h)
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["student_name"] == "Student"
