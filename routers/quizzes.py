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


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit: Optional[int] = None
    due_date: Optional[datetime] = None
    shuffle: Optional[bool] = None
    max_attempts: Optional[int] = None   # 0 = clear limit (unlimited)
    is_exam: Optional[bool] = None


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
    if current_user.role == "student":
        # All key-materials in this course
        key_mats = db.query(models.Material).filter(
            models.Material.course_id == course_id,
            models.Material.unlock_quiz_id.isnot(None),
        ).all()
        # Student's completions for those materials
        if key_mats:
            completed_ids = {
                c.material_id for c in db.query(models.MaterialCompletion).filter(
                    models.MaterialCompletion.student_id == current_user.id,
                    models.MaterialCompletion.material_id.in_([m.id for m in key_mats]),
                ).all()
            }
            # Group by quiz
            from collections import defaultdict
            required: dict = defaultdict(list)
            for m in key_mats:
                required[m.unlock_quiz_id].append(m)
            for quiz_id, mats in required.items():
                missing = [m for m in mats if m.id not in completed_ids]
                if missing:
                    locked_quiz_ids.add(quiz_id)
                    lock_requirements[quiz_id] = [m.title for m in missing]

    result = []
    for q in quizzes:
        # Students only see published quizzes
        if current_user.role == "student" and not q.is_published:
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

    db.commit()
    db.refresh(q)
    return {"id": q.id, "title": q.title, "is_published": q.is_published, "is_exam": q.is_exam}


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

    import sys
    import base64
    from pathlib import Path

    _IMAGE_MIMES = {"image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp"}
    _IMAGE_EXTS  = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

    content_parts: list[str] = []
    image_b64s:    list[str] = []

    for m in materials:
        text = m.content or ""
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
            else:
                try:
                    text = fpath.read_text(encoding="utf-8", errors="ignore")[:8000]
                except Exception:
                    pass
        if text and not text.startswith("[Image"):
            content_parts.append(f"=== {m.title} ===\n{text[:6000]}")

    if not content_parts and not image_b64s:
        raise HTTPException(400, "Selected materials have no readable content")

    combined = "\n\n".join(content_parts)[:20000]
    print(
        f"[AI Generate] quiz_id={quiz_id} materials={len(materials)} "
        f"text_chars={len(combined)} images={len(image_b64s)}",
        file=sys.stderr,
    )

    system_prompt = (
        "You are an expert educator. Your ONLY job is to read the provided course material "
        "(which may include images of textbook pages, handwritten notes, or slides) "
        "and write exam questions that directly reference specific facts, equations, "
        "definitions, and examples visible in that material. "
        "NEVER write generic questions like 'What is the value of x?' — always include the actual "
        "equation or context from the material. NEVER use placeholder answer options like A, B, C, D or 1, 2, 3, 4. "
        "Every question and every answer option must contain real, specific content from the material."
    )

    image_instruction = (
        "The course material is provided as image(s) above. "
        "Read every equation, definition, diagram label, and example visible in the images carefully."
        if image_b64s else
        "Read the course material text carefully."
    )

    prompt_lines = [
        image_instruction,
        "",
        *(["═══ COURSE MATERIAL TEXT ═══", combined, "═══ END ═══", ""] if combined.strip() and not combined.strip().startswith("[Image") else []),
        f"Generate exactly these question counts based on the material:",
        f"  • {data.num_mc} multiple-choice questions (4 answer options each, exactly one correct)",
        f"  • {data.num_tf} true/false questions",
        f"  • {data.num_short} short-answer questions",
        f"  • {data.num_long} long-answer/essay questions",
        "",
        "MANDATORY RULES:",
        "• Include the actual equation, value, or term from the material in each question.",
        "• Multiple-choice options must be real specific answers — numbers, names, or phrases from the material.",
        "• NEVER use 'A', 'B', 'C', 'D' or '1', '2', '3', '4' as option text.",
        "• True/false statements must be a specific factual claim from the material.",
        "• Do NOT invent facts not present in the material.",
        "",
        "Output ONLY a valid JSON array — no markdown, no explanation, no extra text.",
        "Each element must match one of these exact shapes:",
        '{"type":"multiple_choice","question":"<complete question text>","points":2,"options":[{"text":"<specific answer>","correct":true},{"text":"<specific wrong answer>","correct":false},{"text":"<specific wrong answer>","correct":false},{"text":"<specific wrong answer>","correct":false}]}',
        '{"type":"true_false","question":"<specific factual statement>","points":1,"correct":true}',
        '{"type":"short_answer","question":"<complete question text>","points":3}',
        '{"type":"long_answer","question":"<complete essay prompt>","points":10}',
    ]

    model_to_use = VISION_MODEL if image_b64s else None  # None = use OLLAMA_MODEL default
    print(f"[AI Generate] using model={model_to_use or OLLAMA_MODEL}", file=sys.stderr)

    raw = ollama_chat(
        [{"role": "user", "content": "\n".join(prompt_lines)}],
        system=system_prompt,
        images=image_b64s or None,
        model=model_to_use,
        temperature=0.3,
        max_tokens=8192,
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

    # Try direct parse first
    questions_data = None
    try:
        questions_data = json.loads(raw)
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
                db.add(models.QuizOption(
                    question_id=qq.id,
                    option_text=opt.get("text", ""),
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
