"""
question_banks.py — Reusable question pools importable into quizzes.

GET    /api/question-banks/                      List all banks
POST   /api/question-banks/                      Create a bank
GET    /api/question-banks/{id}                  Bank detail + questions
POST   /api/question-banks/{id}/questions        Add a question
DELETE /api/question-banks/{id}                  Delete a bank
POST   /api/question-banks/{id}/import/{quiz_id} Import N random questions
"""
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Any
from database import get_db
import models
import security

router = APIRouter()


class BankCreate(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: Optional[int] = None


class BankQuestionIn(BaseModel):
    question_text: str
    question_type: str  # multiple_choice, true_false, short_answer
    points: float = 1.0
    options: Optional[Any] = None  # list of {text, is_correct}
    tags: Optional[str] = None


@router.get("/")
def list_banks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    banks = db.query(models.QuestionBank).filter(
        models.QuestionBank.creator_id == current_user.id
    ).all()
    if current_user.role == "admin":
        banks = db.query(models.QuestionBank).all()
    return [
        {
            "id": b.id,
            "title": b.title,
            "description": b.description,
            "course_id": b.course_id,
            "question_count": len(b.questions),
            "created_at": str(b.created_at),
        }
        for b in banks
    ]


@router.post("/")
def create_bank(
    data: BankCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    if data.course_id:
        security.require_course_access(data.course_id, current_user, db)
    bank = models.QuestionBank(
        title=data.title,
        description=data.description,
        course_id=data.course_id,
        creator_id=current_user.id,
    )
    db.add(bank)
    db.commit()
    db.refresh(bank)
    return {"id": bank.id, "title": bank.title}


@router.get("/{bank_id}")
def get_bank(
    bank_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    bank = db.query(models.QuestionBank).filter(models.QuestionBank.id == bank_id).first()
    if not bank:
        raise HTTPException(404, "Bank not found")
    if current_user.role != "admin" and bank.creator_id != current_user.id:
        raise HTTPException(403, "Access denied")
    return {
        "id": bank.id,
        "title": bank.title,
        "description": bank.description,
        "course_id": bank.course_id,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "points": q.points,
                "options": q.options,
                "tags": q.tags,
            }
            for q in bank.questions
        ],
    }


@router.delete("/{bank_id}")
def delete_bank(
    bank_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    bank = db.query(models.QuestionBank).filter(models.QuestionBank.id == bank_id).first()
    if not bank:
        raise HTTPException(404, "Bank not found")
    if current_user.role != "admin" and bank.creator_id != current_user.id:
        raise HTTPException(403, "Access denied")
    db.delete(bank)
    db.commit()
    return {"ok": True}


@router.post("/{bank_id}/questions")
def add_questions(
    bank_id: int,
    questions: List[BankQuestionIn],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    bank = db.query(models.QuestionBank).filter(models.QuestionBank.id == bank_id).first()
    if not bank:
        raise HTTPException(404, "Bank not found")
    if current_user.role != "admin" and bank.creator_id != current_user.id:
        raise HTTPException(403, "Access denied")

    added = []
    for q_data in questions:
        q = models.BankQuestion(
            bank_id=bank_id,
            question_text=q_data.question_text,
            question_type=q_data.question_type,
            points=q_data.points,
            options=q_data.options,
            tags=q_data.tags,
        )
        db.add(q)
        db.flush()
        added.append(q.id)

    db.commit()
    return {"added": added}


@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    q = db.query(models.BankQuestion).filter(models.BankQuestion.id == question_id).first()
    if not q:
        raise HTTPException(404, "Question not found")
    bank = db.query(models.QuestionBank).filter(models.QuestionBank.id == q.bank_id).first()
    if current_user.role != "admin" and bank.creator_id != current_user.id:
        raise HTTPException(403, "Access denied")
    db.delete(q)
    db.commit()
    return {"ok": True}


@router.post("/{bank_id}/import/{quiz_id}")
def import_to_quiz(
    bank_id: int,
    quiz_id: int,
    count: int = 5,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    bank = db.query(models.QuestionBank).filter(models.QuestionBank.id == bank_id).first()
    if not bank:
        raise HTTPException(404, "Bank not found")
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(404, "Quiz not found")
    security.require_course_access(quiz.course_id, current_user, db)

    pool = bank.questions
    selected = random.sample(pool, min(count, len(pool)))

    # Find the current max order_num
    existing_count = len(quiz.questions)
    imported = []
    for i, bq in enumerate(selected):
        qq = models.QuizQuestion(
            quiz_id=quiz_id,
            question_text=bq.question_text,
            question_type=bq.question_type,
            points=bq.points,
            order_num=existing_count + i,
        )
        db.add(qq)
        db.flush()
        # Add options if available
        if bq.options:
            for opt in bq.options:
                option = models.QuizOption(
                    question_id=qq.id,
                    option_text=opt.get("text", ""),
                    is_correct=opt.get("is_correct", False),
                )
                db.add(option)
        imported.append(qq.id)

    db.commit()
    return {"imported": len(imported), "question_ids": imported}
