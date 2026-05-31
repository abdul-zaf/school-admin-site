from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from database import get_db
import models
import security

router = APIRouter()


# ── Schemas ──────────────────────────────────────────────────────────────────

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None
    time_limit: Optional[int] = None
    due_date: Optional[datetime] = None
    shuffle: bool = False


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit: Optional[int] = None
    due_date: Optional[datetime] = None
    shuffle: Optional[bool] = None


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
            "is_published": q.is_published,
            "question_count": len(q.questions),
            "total_points": sum(qq.points for qq in q.questions),
            "attempt_count": len(q.attempts) if current_user.role in ("admin", "teacher") else None,
            "my_attempt": my_attempt,
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

    db.commit()
    db.refresh(q)
    return {"id": q.id, "title": q.title, "is_published": q.is_published}


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

    q.is_published = data.is_published
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

    # Auto-grade MC & True/False; flag short_answer for manual grading
    total_score = 0.0
    has_short = False
    for ans in data.answers:
        qq = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == ans.question_id).first()
        if not qq:
            continue
        if qq.question_type == "short_answer":
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
    return {
        "score": attempt.score,
        "total_possible": total_possible,
        "has_short_answer": has_short,
        "submitted": True,
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
    return [
        {
            "id": a.id,
            "student_name": a.student.name,
            "student_id": a.student_id,
            "started_at": str(a.started_at),
            "submitted_at": str(a.submitted_at) if a.submitted_at else None,
            "score": a.score,
            "total_possible": total_possible,
        }
        for a in attempts
    ]
