"""
quizzes.py — Full quiz lifecycle: build, publish, attempt, auto-grade.

GET    /api/quizzes/course/{id}     List quizzes (students: published only)
POST   /api/quizzes/course/{id}     Create quiz as draft (teacher/admin)
GET    /api/quizzes/{id}            Quiz detail with questions + my attempt
PUT    /api/quizzes/{id}            Edit quiz metadata
PATCH  /api/quizzes/{id}/publish    Toggle published state
DELETE /api/quizzes/{id}            Delete quiz
POST   /api/quizzes/{id}/questions  Add a question (MC / T-F / short-answer)
DELETE /api/quizzes/questions/{id}  Delete a question (own course only)
POST   /api/quizzes/{id}/start      Start an attempt (checks retake limit)
POST   /api/quizzes/{id}/submit     Submit answers; MC/T-F auto-graded
GET    /api/quizzes/{id}/attempts   All student attempts (teacher/admin)
"""
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from database import get_db
import models
import security
from routers.notifications import notify as push_notif

router = APIRouter()


# ── Schemas ──────────────────────────────────────────────────────────────────

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None
    time_limit: Optional[int] = None
    due_date: Optional[datetime] = None
    shuffle: bool = False
    max_attempts: Optional[int] = None   # None = unlimited
    is_exam: bool = False
    unlock_all_materials: bool = False


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit: Optional[int] = None
    due_date: Optional[datetime] = None
    shuffle: Optional[bool] = None
    max_attempts: Optional[int] = None   # 0 = clear limit (unlimited)
    is_exam: Optional[bool] = None
    unlock_all_materials: Optional[bool] = None


class PublishToggle(BaseModel):
    is_published: bool


class OptionCreate(BaseModel):
    option_text: str
    is_correct: bool = False


class QuestionCreate(BaseModel):
    question_text: str
    question_type: str          # multiple_choice | true_false | short_answer
    points: float = 1.0
    options: List[OptionCreate] = []


class AnswerSubmit(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None
    text_answer: Optional[str] = None


class QuizSubmit(BaseModel):
    answers: List[AnswerSubmit]


# ── Helpers ───────────────────────────────────────────────────────────────────

def serialise_quiz(q: models.Quiz, hide_correct: bool = True, my_attempt=None):
    return {
        "id": q.id,
        "course_id": q.course_id,
        "title": q.title,
        "description": q.description,
        "time_limit": q.time_limit,
        "due_date": str(q.due_date) if q.due_date else None,
        "shuffle": q.shuffle,
        "is_published": q.is_published,
        "max_attempts": q.max_attempts,
        "is_exam": q.is_exam,
        "unlock_all_materials": q.unlock_all_materials,
        "created_at": str(q.created_at),
        "question_count": len(q.questions),
        "total_points": sum(qq.points for qq in q.questions),
        "my_attempt": my_attempt,
        "questions": [
            {
                "id": qq.id,
                "question_text": qq.question_text,
                "question_type": qq.question_type,
                "points": qq.points,
                "order_num": qq.order_num,
                "options": [
                    {
                        "id": o.id,
                        "option_text": o.option_text,
                        **({"is_correct": o.is_correct} if not hide_correct else {}),
                    }
                    for o in qq.options
                ],
            }
            for qq in q.questions
        ],
    }


# ── Quiz CRUD ─────────────────────────────────────────────────────────────────

@router.get("/course/{course_id}")
def list_quizzes(
    course_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    quizzes = db.query(models.Quiz).filter(models.Quiz.course_id == course_id).all()

    # Build per-student unlock state: which quiz ids are still locked
    locked_quiz_ids: set = set()
    lock_requirements: dict = {}  # quiz_id -> list of required material titles
    all_materials_completed: bool = False  # True when student has finished every material
    if current_user.role == "student":
        # ── Per-material unlock (unlock_quiz_id on Material) ─────────────────
        key_mats = db.query(models.Material).filter(
            models.Material.course_id == course_id,
            models.Material.unlock_quiz_id.isnot(None),
        ).all()
        if key_mats:
            completed_ids = {
                c.material_id for c in db.query(models.MaterialCompletion).filter(
                    models.MaterialCompletion.student_id == current_user.id,
                    models.MaterialCompletion.material_id.in_([m.id for m in key_mats]),
                ).all()
            }
            from collections import defaultdict
            required: dict = defaultdict(list)
            for m in key_mats:
                required[m.unlock_quiz_id].append(m)
            for qid, mats in required.items():
                missing = [m for m in mats if m.id not in completed_ids]
                if missing:
                    locked_quiz_ids.add(qid)
                    lock_requirements[qid] = [m.title for m in missing]

        # ── All-materials unlock (unlock_all_materials on Quiz) ───────────────
        all_mats = db.query(models.Material).filter(
            models.Material.course_id == course_id,
        ).all()
        if all_mats:
            all_mat_ids = {m.id for m in all_mats}
            done_ids = {
                c.material_id for c in db.query(models.MaterialCompletion).filter(
                    models.MaterialCompletion.student_id == current_user.id,
                    models.MaterialCompletion.material_id.in_(list(all_mat_ids)),
                ).all()
            }
            all_materials_completed = all_mat_ids.issubset(done_ids)
        else:
            # No materials in course → treat as "all done" so the exam is visible
            all_materials_completed = True

    result = []
    for q in quizzes:
        # Students only see published quizzes
        if current_user.role == "student" and not q.is_published:
            continue

        # Hide all-materials-gated exams from students who haven't finished all materials
        if current_user.role == "student" and q.unlock_all_materials and not all_materials_completed:
            continue

        # Hide per-material-gated quizzes from students who haven't completed the required material
        if current_user.role == "student" and q.id in locked_quiz_ids:
            continue

        my_attempt = None
        if current_user.role == "student":
            a = db.query(models.QuizAttempt).filter(
                models.QuizAttempt.quiz_id == q.id,
                models.QuizAttempt.student_id == current_user.id,
            ).first()
            if a:
                my_attempt = {
                    "id": a.id,
                    "submitted_at": str(a.submitted_at) if a.submitted_at else None,
                    "score": a.score,
                }
        result.append({
            "id": q.id,
            "title": q.title,
            "description": q.description,
            "time_limit": q.time_limit,
            "due_date": str(q.due_date) if q.due_date else None,
            "is_published":  q.is_published,
            "max_attempts":  q.max_attempts,
            "is_exam": q.is_exam,
            "unlock_all_materials": q.unlock_all_materials,
            "question_count": len(q.questions),
            "total_points":  sum(qq.points for qq in q.questions),
            "attempt_count": len(q.attempts) if current_user.role in ("admin", "teacher") else None,
            "attempts_used": sum(1 for a in q.attempts if a.student_id == current_user.id)
                             if current_user.role == "student" else None,
            "my_attempt": my_attempt,
            # Unlock fields (students only)
            "is_locked": q.id in locked_quiz_ids,
            "lock_requires": lock_requirements.get(q.id, []),
        })
    return result


@router.post("/course/{course_id}")
def create_quiz(
    course_id: int,
    data: QuizCreate,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    q = models.Quiz(
        course_id=course_id,
        title=data.title,
        description=data.description,
        time_limit=data.time_limit,
        due_date=data.due_date,
        shuffle=data.shuffle,
        max_attempts=data.max_attempts,
        is_exam=data.is_exam,
        unlock_all_materials=data.unlock_all_materials,
        is_published=False,  # always starts as draft
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return {"id": q.id, "title": q.title}


@router.get("/{quiz_id}")
def get_quiz(
    quiz_id: int,
    mode: str = "take",
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    q = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not q:
        raise HTTPException(404, "Quiz not found")

    is_teacher = current_user.role in ("admin", "teacher")

    if current_user.role == "student":
        # Gate: per-material-gated quiz — locked until the student completes the required material
        gate_mat = db.query(models.Material).filter(
            models.Material.course_id == q.course_id,
            models.Material.unlock_quiz_id == q.id,
        ).first()
        if gate_mat:
            completed = db.query(models.MaterialCompletion).filter(
                models.MaterialCompletion.student_id == current_user.id,
                models.MaterialCompletion.material_id == gate_mat.id,
            ).first()
            if not completed:
                raise HTTPException(404, "Quiz not found")

        # Gate: all-materials-gated exam — locked until the student finishes every material
        if q.unlock_all_materials:
            all_mats = db.query(models.Material).filter(
                models.Material.course_id == q.course_id,
            ).all()
            if all_mats:
                all_mat_ids = {m.id for m in all_mats}
                done_ids = {
                    c.material_id for c in db.query(models.MaterialCompletion).filter(
                        models.MaterialCompletion.student_id == current_user.id,
                        models.MaterialCompletion.material_id.in_(list(all_mat_ids)),
                    ).all()
                }
                if not all_mat_ids.issubset(done_ids):
                    raise HTTPException(404, "Quiz not found")

    my_attempt = None
    hide_correct = not is_teacher

    if current_user.role == "student":
        a = db.query(models.QuizAttempt).filter(
            models.QuizAttempt.quiz_id == quiz_id,
            models.QuizAttempt.student_id == current_user.id,
        ).first()
        if a:
            my_attempt = {
                "id": a.id,
                "started_at": str(a.started_at),
                "submitted_at": str(a.submitted_at) if a.submitted_at else None,
                "score": a.score,
                "answers": [
                    {
                        "question_id": ans.question_id,
                        "selected_option_id": ans.selected_option_id,
                        "text_answer": ans.text_answer,
                        "teacher_score": ans.teacher_score,
                        "teacher_feedback": ans.teacher_feedback,
                    }
                    for ans in a.answers
                ],
            }
            if a.submitted_at:
                hide_correct = False   # reveal answers after submission

    return serialise_quiz(q, hide_correct=hide_correct, my_attempt=my_attempt)


@router.put("/{quiz_id}")
def update_quiz(
    quiz_id: int,
    data: QuizUpdate,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    q = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not q:
        raise HTTPException(404, "Quiz not found")
    security.require_course_access(q.course_id, current_user, db)

    if data.title is not None:
        q.title = data.title
    if data.description is not None:
        q.description = data.description
    if data.time_limit is not None:
        q.time_limit = data.time_limit if data.time_limit > 0 else None
    if data.due_date is not None:
        q.due_date = data.due_date
    if data.shuffle is not None:
        q.shuffle = data.shuffle
    if data.max_attempts is not None:
        q.max_attempts = None if data.max_attempts == 0 else data.max_attempts
    if data.is_exam is not None:
        q.is_exam = data.is_exam
    if data.unlock_all_materials is not None:
        q.unlock_all_materials = data.unlock_all_materials

    db.commit()
    db.refresh(q)
    return {"id": q.id, "title": q.title, "is_published": q.is_published, "is_exam": q.is_exam, "unlock_all_materials": q.unlock_all_materials}


@router.patch("/{quiz_id}/publish")
def toggle_publish(
    quiz_id: int,
    data: PublishToggle,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    q = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not q:
        raise HTTPException(404, "Quiz not found")
    security.require_course_access(q.course_id, current_user, db)

    if data.is_published and len(q.questions) == 0:
        raise HTTPException(400, "Cannot publish a quiz with no questions. Add at least one question first.")

    was_published = q.is_published
    q.is_published = data.is_published
    db.commit()

    # Notify enrolled students only when going from draft → published
    if data.is_published and not was_published:
        course = db.query(models.Course).filter(models.Course.id == q.course_id).first()
        course_title = course.title if course else "your course"
        enrollments = db.query(models.Enrollment).filter(models.Enrollment.course_id == q.course_id).all()
        for enr in enrollments:
            push_notif(db, enr.student_id, "quiz",
                       f"📝 New quiz available: {q.title}",
                       course_title,
                       link=f"quiz:{q.id}")
        db.commit()

    return {"id": q.id, "is_published": q.is_published}


@router.delete("/{quiz_id}")
def delete_quiz(
    quiz_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    q = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not q:
        raise HTTPException(404, "Quiz not found")
    security.require_course_access(q.course_id, current_user, db)
    db.delete(q)
    db.commit()
    return {"ok": True}


# ── Questions ─────────────────────────────────────────────────────────────────

@router.post("/{quiz_id}/questions")
def add_question(
    quiz_id: int,
    data: QuestionCreate,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    q = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not q:
        raise HTTPException(404, "Quiz not found")
    security.require_course_access(q.course_id, current_user, db)

    question = models.QuizQuestion(
        quiz_id=quiz_id,
        question_text=data.question_text,
        question_type=data.question_type,
        points=data.points,
        order_num=len(q.questions),
    )
    db.add(question)
    db.flush()

    for opt in data.options:
        db.add(models.QuizOption(
            question_id=question.id,
            option_text=opt.option_text,
            is_correct=opt.is_correct,
        ))

    db.commit()
    db.refresh(question)
    return {"id": question.id}


@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    qq = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == question_id).first()
    if not qq:
        raise HTTPException(404, "Question not found")
    # Verify the caller owns the quiz's course (prevents cross-teacher deletion)
    security.require_course_access(qq.quiz.course_id, current_user, db)
    db.delete(qq)
    db.commit()
    return {"ok": True}


# ── Student: Start / Submit / Results ────────────────────────────────────────

@router.post("/{quiz_id}/start")
def start_quiz(
    quiz_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    q = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not q:
        raise HTTPException(404, "Quiz not found")
    if not q.is_published:
        raise HTTPException(403, "This quiz is not yet available.")

    existing = db.query(models.QuizAttempt).filter(
        models.QuizAttempt.quiz_id == quiz_id,
        models.QuizAttempt.student_id == current_user.id,
    ).first()

    if existing and existing.submitted_at:
        raise HTTPException(400, "Already submitted")
    if existing:
        return {"attempt_id": existing.id, "started_at": str(existing.started_at)}

    # Enforce retake limit
    if q.max_attempts is not None:
        used = db.query(models.QuizAttempt).filter(
            models.QuizAttempt.quiz_id    == quiz_id,
            models.QuizAttempt.student_id == current_user.id,
        ).count()
        if used >= q.max_attempts:
            raise HTTPException(
                403,
                f"You have used all {q.max_attempts} allowed attempt(s) for this quiz.",
            )

    attempt = models.QuizAttempt(quiz_id=quiz_id, student_id=current_user.id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {"attempt_id": attempt.id, "started_at": str(attempt.started_at)}


@router.post("/{quiz_id}/submit")
def submit_quiz(
    quiz_id: int,
    data: QuizSubmit,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    attempt = db.query(models.QuizAttempt).filter(
        models.QuizAttempt.quiz_id == quiz_id,
        models.QuizAttempt.student_id == current_user.id,
    ).first()
    if not attempt:
        raise HTTPException(400, "Quiz not started. Call /start first.")
    if attempt.submitted_at:
        raise HTTPException(400, "Already submitted")

    # Persist answers
    for ans in data.answers:
        db.add(models.QuizAnswer(
            attempt_id=attempt.id,
            question_id=ans.question_id,
            selected_option_id=ans.selected_option_id,
            text_answer=ans.text_answer,
        ))
    db.flush()

    # Auto-grade MC & True/False; flag short_answer/long_answer for manual grading
    total_score = 0.0
    has_short = False
    for ans in data.answers:
        qq = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == ans.question_id).first()
        if not qq:
            continue
        if qq.question_type in ("short_answer", "long_answer"):
            has_short = True
        elif ans.selected_option_id:
            opt = db.query(models.QuizOption).filter(
                models.QuizOption.id == ans.selected_option_id
            ).first()
            if opt and opt.is_correct:
                total_score += qq.points

    attempt.submitted_at = datetime.utcnow()
    if not has_short:
        attempt.score = total_score

    db.commit()

    quiz_obj = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    total_possible = sum(qq.points for qq in quiz_obj.questions)

    # Record XP, streak, and notify teacher
    try:
        from routers.streaks import record_activity
        from routers.xp import award_xp
        record_activity(db, current_user.id)
        award_xp(db, current_user.id, "quiz_submission", f"Completed quiz: {quiz_obj.title}")
        course = db.query(models.Course).filter(models.Course.id == quiz_obj.course_id).first()
        if course:
            push_notif(db, course.teacher_id, "submission",
                       f"{current_user.name} submitted a quiz",
                       f'"{quiz_obj.title}" in {course.title}',
                       f"courses?id={course.id}")
        db.commit()
    except Exception:
        pass
    return {
        "score": attempt.score,
        "total_possible": total_possible,
        "has_short_answer": has_short,
        "submitted": True,
    }


@router.post("/{quiz_id}/auto-grade-short/{attempt_id}")
def auto_grade_short_answers(
    quiz_id: int,
    attempt_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Use a local Ollama model to grade short_answer questions in an attempt."""
    import json
    from services.ollama import generate as ollama_generate, is_available as ollama_available, OLLAMA_MODEL

    if not ollama_available():
        raise HTTPException(
            503,
            "AI grading is not available. Make sure Ollama is running "
            f"(ollama serve) and '{OLLAMA_MODEL}' is pulled (ollama pull {OLLAMA_MODEL}).",
        )

    attempt = db.query(models.QuizAttempt).filter(
        models.QuizAttempt.id == attempt_id,
        models.QuizAttempt.quiz_id == quiz_id,
    ).first()
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    quiz_obj = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz_obj:
        raise HTTPException(404, "Quiz not found")
    security.require_course_access(quiz_obj.course_id, current_user, db)

    short_answers = [
        ans for ans in attempt.answers
        if ans.question and ans.question.question_type == "short_answer"
    ]
    if not short_answers:
        return {"message": "No short answer questions to grade", "score": attempt.score}

    graded_score = 0.0
    results = []
    for ans in short_answers:
        qq = ans.question
        prompt = (
            f"You are grading a student's short-answer quiz question.\n\n"
            f"Question: {qq.question_text}\n"
            f"Student's answer: {ans.text_answer or '(no answer)'}\n"
            f"Maximum points: {qq.points}\n\n"
            f"Grade this answer from 0 to {qq.points} points. "
            f"Respond with ONLY a JSON object like this (no extra text): "
            f'{{\"score\": <number>, \"feedback\": \"<brief feedback>\"}}'
        )
        try:
            raw = ollama_generate(prompt, max_tokens=200)
            # Strip any markdown code fences the model might add
            raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            graded = json.loads(raw)
            pts = min(float(graded.get("score", 0)), qq.points)
        except Exception:
            pts = 0.0
            graded = {"score": 0, "feedback": "Grading failed"}
        graded_score += pts
        results.append({
            "question_id": qq.id,
            "question_text": qq.question_text,
            "student_answer": ans.text_answer,
            "awarded_points": pts,
            "max_points": qq.points,
            "feedback": graded.get("feedback", ""),
        })

    # Add auto-graded short answer score to the existing MC/TF score
    mc_score = sum(
        qq.points for ans in attempt.answers
        if ans.question and ans.question.question_type != "short_answer" and ans.selected_option
        for opt in [db.query(models.QuizOption).filter(models.QuizOption.id == ans.selected_option_id).first()]
        if opt and opt.is_correct
        for qq in [ans.question]
    )
    attempt.score = mc_score + graded_score
    db.commit()

    return {
        "attempt_id": attempt_id,
        "total_score": attempt.score,
        "short_answer_results": results,
    }


@router.get("/{quiz_id}/attempts")
def get_attempts(
    quiz_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    quiz_obj = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    total_possible = sum(qq.points for qq in quiz_obj.questions) if quiz_obj else 0
    attempts = db.query(models.QuizAttempt).filter(models.QuizAttempt.quiz_id == quiz_id).all()
    result = []
    for a in attempts:
        needs_grading = a.submitted_at and a.score is None
        result.append({
            "id": a.id,
            "student_name": a.student.name,
            "student_id": a.student_id,
            "started_at": str(a.started_at),
            "submitted_at": str(a.submitted_at) if a.submitted_at else None,
            "score": a.score,
            "total_possible": total_possible,
            "needs_grading": needs_grading,
        })
    return result


# ── AI-generate questions from selected materials ─────────────────────────────

class AIGenerateRequest(BaseModel):
    material_ids: List[int]
    num_mc: int = 5
    num_tf: int = 3
    num_short: int = 2
    num_long: int = 1


@router.post("/{quiz_id}/ai-generate")
def ai_generate_questions(
    quiz_id: int,
    data: AIGenerateRequest,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Generate quiz questions from course materials using Ollama."""
    import json
    from services.ollama import chat as ollama_chat, is_available as ollama_available, OLLAMA_MODEL

    # Vision model to use when materials contain images.
    # llava is a well-known vision model; fall back to env-configured model if not available.
    VISION_MODEL = os.getenv("OLLAMA_VISION_MODEL", "llava")

    if not ollama_available():
        raise HTTPException(
            503,
            "AI generation requires Ollama to be running. "
            "Start it with `ollama serve` and make sure a model is pulled.",
        )

    quiz_obj = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz_obj:
        raise HTTPException(404, "Quiz not found")
    security.require_course_access(quiz_obj.course_id, current_user, db)

    # Load material content
    materials = db.query(models.Material).filter(
        models.Material.id.in_(data.material_ids),
        models.Material.course_id == quiz_obj.course_id,
    ).all()
    if not materials:
        raise HTTPException(400, "No valid materials selected")

    import re as _re
    import sys
    import base64
    from pathlib import Path

    _IMAGE_MIMES = {"image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp"}
    _IMAGE_EXTS  = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

    def _extract_equations(text: str) -> list[str]:
        """Pull out lines/segments that look like mathematical equations or formulas."""
        eq_lines = []
        # Whole lines that contain =, ≠, ≤, ≥, ±, math operators, or common formula patterns
        eq_pattern = _re.compile(
            r'(?:'
            r'[A-Za-z0-9_α-ωΑ-Ω]+\s*[=≠≤≥<>]\s*[^\n]{1,120}'   # x = ..., F = ma
            r'|[A-Za-zα-ω]+\^[0-9]'                                          # x^2, v^2
            r'|√[^\s]+'                                                                  # √something
            r'|\d+\s*[×÷\*/]\s*\d+'                                                     # 3 × 4
            r'|\bintegral\b|\bderivative\b|\blimit\b|\bsum\b'                            # calculus words
            r'|\b(?:sin|cos|tan|log|ln|exp)\s*[\(\[]'                                   # trig/log fns
            r')'
        )
        for line in text.splitlines():
            stripped = line.strip()
            if stripped and eq_pattern.search(stripped):
                eq_lines.append(stripped)
        # Also pull inline patterns like "F = ma" from prose
        inline = _re.findall(
            r'\b[A-Za-z_]{1,4}\s*=\s*[A-Za-z0-9_\+\-\*/\^\(\)\s\.]{2,40}(?=[\.,;\n]|$)',
            text
        )
        eq_lines.extend(inline)
        # Deduplicate while preserving order
        seen: set[str] = set()
        result = []
        for e in eq_lines:
            key = e.strip()
            if key and key not in seen:
                seen.add(key)
                result.append(key)
        return result[:60]  # cap to avoid bloating prompt

    content_parts: list[str] = []
    image_b64s:    list[str] = []
    all_equations: list[str] = []

    for m in materials:
        text = m.content or ""
        if m.material_type == "link":
            # URL-only materials have no extractable text; note it for transparency
            content_parts.append(f"=== {m.title} ===\n[External link — no text content available]")
            continue
        if m.material_type == "file" and m.file_path:
            fpath = Path(m.file_path)
            mime  = (m.file_mime or "").lower()
            ext   = fpath.suffix.lower()
            is_image = mime in _IMAGE_MIMES or ext in _IMAGE_EXTS
            if is_image:
                try:
                    image_b64s.append(base64.b64encode(fpath.read_bytes()).decode())
                    content_parts.append(f"[Image material: {m.title}]")
                except Exception as exc:
                    print(f"[AI Generate] could not read image {fpath}: {exc}", file=sys.stderr)
                continue
            else:
                try:
                    text = fpath.read_text(encoding="utf-8", errors="ignore")[:3000]
                except Exception:
                    pass
        if text and not text.startswith("[Image"):
            eqs = _extract_equations(text)
            all_equations.extend(eqs)
            content_parts.append(f"=== {m.title} ===\n{text[:3000]}")

    if not content_parts and not image_b64s:
        raise HTTPException(400, "Selected materials have no readable content")

    combined = "\n\n".join(content_parts)[:12000]
    print(
        f"[AI Generate] quiz_id={quiz_id} materials={len(materials)} "
        f"text_chars={len(combined)} images={len(image_b64s)} equations={len(all_equations)}",
        file=sys.stderr,
    )

    # Build a deduplicated equation reference block
    unique_eqs = list(dict.fromkeys(e.strip() for e in all_equations if e.strip()))
    eq_block = ""
    if unique_eqs:
        eq_block = (
            "═══ EQUATIONS / FORMULAS EXTRACTED FROM MATERIAL ═══\n"
            + "\n".join(f"  • {e}" for e in unique_eqs[:50])
            + "\n═══ END EQUATIONS ═══"
        )

    system_prompt = (
        "You are an expert educator writing exam questions. "
        "You are given course material text and, separately, a list of every equation and formula "
        "found in that material. "
        "Your ONLY job is to write questions that test the specific facts, equations, definitions, "
        "and examples from the provided material. "
        "EQUATIONS: every equation or formula listed MUST appear verbatim inside at least one question "
        "or answer option — copy the exact symbols, variables, and notation. "
        "NEVER write generic questions like 'Solve for x' or 'What is the formula?' — "
        "always embed the actual equation from the material (e.g. 'Given F = ma, if m = 5 kg and a = 3 m/s², what is F?'). "
        "NEVER use placeholder answer options like A, B, C, D or 1, 2, 3, 4. "
        "Every answer option must contain a real value, expression, or phrase from the material. "
        "NEVER ask about people's names, teacher names, student names, course names, school names, "
        "dates of enrollment, administrative details, or anything not directly about the subject matter. "
        "Every question must test understanding of a concept, fact, or calculation from the material — "
        "not metadata about the course or who teaches it."
    )

    image_instruction = (
        "The course material is provided as image(s) above. "
        "Read every equation, definition, diagram label, and example visible in the images carefully. "
        "Copy equations exactly as they appear."
        if image_b64s else
        "Read the course material text and the extracted equation list carefully."
    )

    prompt_lines = [
        image_instruction,
        "",
        *(["═══ COURSE MATERIAL TEXT ═══", combined, "═══ END MATERIAL ═══", ""] if combined.strip() and not combined.strip().startswith("[Image") else []),
        *([eq_block, ""] if eq_block else []),
        f"Generate exactly these question counts based solely on the material above:",
        f"  • {data.num_mc} multiple-choice questions (4 answer options each, exactly one correct)",
        f"  • {data.num_tf} true/false questions",
        f"  • {data.num_short} short-answer questions",
        f"  • {data.num_long} long-answer/essay questions",
        "",
        "MANDATORY RULES:",
        "• Equations/formulas: embed them verbatim in the question text (e.g. 'Using v² = u² + 2as, find v when...').",
        "• Multiple-choice options must be real, specific values/expressions — never generic labels.",
        "• For math/science questions, all numerical answer options MUST be whole integers (e.g. 10, 25, 100) — never decimals like 10.0 or 2.5 unless the material explicitly uses decimals.",
        "• True/false statements must make a precise factual or mathematical claim from the material.",
        "• Short/long-answer questions must name the specific concept, equation, or scenario from the material.",
        "• Do NOT invent facts, values, or equations not present in the material.",
        "• Do NOT ask about names of teachers, students, schools, or any administrative/metadata details.",
        "• Every question must test subject knowledge only — concepts, calculations, definitions, or examples from the material.",
        "",
        "Output ONLY a valid JSON array — no markdown, no explanation, no extra text.",
        "Each element must match one of these exact shapes:",
        '{"type":"multiple_choice","question":"<full question including equation>","points":2,"options":[{"text":"<specific value or expression>","correct":true},{"text":"<wrong value>","correct":false},{"text":"<wrong value>","correct":false},{"text":"<wrong value>","correct":false}]}',
        '{"type":"true_false","question":"<precise factual claim from material>","points":1,"correct":true}',
        '{"type":"short_answer","question":"<full question referencing specific content>","points":3}',
        '{"type":"long_answer","question":"<essay prompt referencing specific concepts>","points":10}',
    ]

    model_to_use = VISION_MODEL if image_b64s else None  # None = use OLLAMA_MODEL default
    print(f"[AI Generate] using model={model_to_use or OLLAMA_MODEL}", file=sys.stderr)

    raw = ollama_chat(
        [{"role": "user", "content": "\n".join(prompt_lines)}],
        system=system_prompt,
        images=image_b64s or None,
        model=model_to_use,
        temperature=0.3,
        max_tokens=2048,
        num_ctx=4096,
    )

    # Log raw response for debugging
    print(f"[AI Generate] raw response (first 500 chars): {raw[:500]!r}", file=sys.stderr)

    # Strip markdown fences (```json ... ``` or ``` ... ```)
    raw = raw.strip()
    if raw.startswith("```"):
        # Remove opening fence line
        first_newline = raw.find("\n")
        raw = raw[first_newline + 1:] if first_newline != -1 else raw[3:]
        # Remove closing fence
        if raw.endswith("```"):
            raw = raw[:-3].strip()

    raw = raw.strip()

    def _repair_json(s: str) -> str:
        """Fix AI JSON that omits closing } on option objects.

        The model produces lines like:
            {"text": "6 + 4 = 10",      <- should be {"text":"6 + 4 = 10"},
            {"text": "3 - 5 = 8",       <- same
        i.e. each option object is missing its closing } and the comma
        is stuck inside the object rather than between objects.
        Strategy: walk line-by-line and track brace depth; if a line
        opens a { but doesn't close it, and the next non-empty line
        opens another { or is ], auto-close the current object.
        """
        lines = s.splitlines()
        out = []
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.rstrip()
            # Count unmatched braces on this line (ignoring strings)
            # Simple heuristic: count { and } outside quoted strings
            depth = 0
            in_str = False
            esc = False
            for ch in stripped:
                if esc:
                    esc = False
                    continue
                if ch == '\\' and in_str:
                    esc = True
                    continue
                if ch == '"':
                    in_str = not in_str
                    continue
                if not in_str:
                    if ch == '{':
                        depth += 1
                    elif ch == '}':
                        depth -= 1

            # If line has net open brace(s), peek at the next non-empty line
            if depth > 0:
                # Find next non-empty line
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                next_stripped = lines[j].strip() if j < len(lines) else ''
                # If next line starts a new object or closes an array, auto-close
                if next_stripped.startswith('{') or next_stripped.startswith(']'):
                    # Remove trailing comma from this line if present, add }
                    if stripped.endswith(','):
                        stripped = stripped[:-1] + '},'
                    else:
                        stripped = stripped + '}'
                    line = line[:len(line) - len(line.rstrip())] + stripped

            out.append(line)
            i += 1
        return '\n'.join(out)

    # Try direct parse first
    questions_data = None
    try:
        questions_data = json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try repairing common AI JSON mistakes
    if questions_data is None:
        try:
            questions_data = json.loads(_repair_json(raw))
        except json.JSONDecodeError:
            pass

    # Fall back: find the outermost [ ... ] in the response
    if questions_data is None:
        import re
        m = re.search(r'(\[[\s\S]*\])', raw)
        if m:
            try:
                questions_data = json.loads(m.group(1))
            except json.JSONDecodeError:
                # Try repair on the extracted block too
                try:
                    questions_data = json.loads(_repair_json(m.group(1)))
                except json.JSONDecodeError:
                    pass

    if questions_data is None:
        print(f"[AI Generate] FULL raw response: {raw!r}", file=sys.stderr)
        raise HTTPException(500, f"AI returned invalid JSON. Raw (truncated): {raw[:300]}")

    if not isinstance(questions_data, list):
        raise HTTPException(500, "AI response was not a JSON array. Try again.")

    created = []
    for i, qd in enumerate(questions_data):
        qtype = qd.get("type", "short_answer")
        if qtype not in ("multiple_choice", "true_false", "short_answer", "long_answer"):
            continue
        qq = models.QuizQuestion(
            quiz_id=quiz_id,
            question_text=qd.get("question", "").strip(),
            question_type=qtype,
            points=float(qd.get("points", 1)),
            order_num=len(quiz_obj.questions) + i,
        )
        db.add(qq)
        db.flush()

        if qtype == "multiple_choice":
            for opt in qd.get("options", []):
                raw_text = str(opt.get("text", "")).strip()
                # Remove trailing .0 from whole-number decimals (e.g. "10.0" → "10")
                try:
                    fval = float(raw_text)
                    if fval == int(fval):
                        raw_text = str(int(fval))
                except (ValueError, OverflowError):
                    pass
                db.add(models.QuizOption(
                    question_id=qq.id,
                    option_text=raw_text,
                    is_correct=bool(opt.get("correct", False)),
                ))
        elif qtype == "true_false":
            correct = bool(qd.get("correct", True))
            db.add(models.QuizOption(question_id=qq.id, option_text="True", is_correct=correct))
            db.add(models.QuizOption(question_id=qq.id, option_text="False", is_correct=not correct))

        created.append(qq.id)

    db.commit()
    return {"created": len(created), "question_ids": created}


# ── Teacher grading for long-answer questions ─────────────────────────────────

class LongAnswerGrade(BaseModel):
    answer_id: int
    score: float
    feedback: Optional[str] = None


class GradeAttemptRequest(BaseModel):
    grades: List[LongAnswerGrade]


@router.post("/{quiz_id}/grade-attempt/{attempt_id}")
def grade_long_answers(
    quiz_id: int,
    attempt_id: int,
    data: GradeAttemptRequest,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Teacher submits scores for long-answer questions in an attempt."""
    quiz_obj = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz_obj:
        raise HTTPException(404, "Quiz not found")
    security.require_course_access(quiz_obj.course_id, current_user, db)

    attempt = db.query(models.QuizAttempt).filter(
        models.QuizAttempt.id == attempt_id,
        models.QuizAttempt.quiz_id == quiz_id,
    ).first()
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    # Build lookup for this attempt's answers
    answer_map = {a.id: a for a in attempt.answers}

    for g in data.grades:
        ans = answer_map.get(g.answer_id)
        if not ans:
            continue
        qq = ans.question
        if not qq or qq.question_type not in ("short_answer", "long_answer"):
            continue
        ans.teacher_score = min(g.score, qq.points)
        ans.teacher_feedback = g.feedback

    # Recompute total score: auto-graded MC/TF + teacher-graded text answers
    total = 0.0
    all_graded = True
    for ans in attempt.answers:
        qq = ans.question
        if not qq:
            continue
        if qq.question_type in ("short_answer", "long_answer"):
            if ans.teacher_score is not None:
                total += ans.teacher_score
            else:
                all_graded = False
        elif ans.selected_option_id:
            opt = db.query(models.QuizOption).filter(
                models.QuizOption.id == ans.selected_option_id
            ).first()
            if opt and opt.is_correct:
                total += qq.points

    if all_graded:
        attempt.score = total

    db.commit()

    return {
        "attempt_id": attempt_id,
        "score": attempt.score,
        "fully_graded": all_graded,
    }


@router.get("/{quiz_id}/attempt/{attempt_id}/long-answers")
def get_long_answers(
    quiz_id: int,
    attempt_id: int,
    db: DBSession = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Get all long/short answer responses for a specific attempt (for teacher grading)."""
    quiz_obj = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz_obj:
        raise HTTPException(404, "Quiz not found")
    security.require_course_access(quiz_obj.course_id, current_user, db)

    attempt = db.query(models.QuizAttempt).filter(
        models.QuizAttempt.id == attempt_id,
        models.QuizAttempt.quiz_id == quiz_id,
    ).first()
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    results = []
    for ans in attempt.answers:
        qq = ans.question
        if qq and qq.question_type in ("short_answer", "long_answer"):
            results.append({
                "answer_id": ans.id,
                "question_id": qq.id,
                "question_text": qq.question_text,
                "question_type": qq.question_type,
                "max_points": qq.points,
                "student_answer": ans.text_answer or "",
                "teacher_score": ans.teacher_score,
                "teacher_feedback": ans.teacher_feedback,
            })

    return {
        "attempt_id": attempt_id,
        "student_name": attempt.student.name,
        "answers": results,
    }
