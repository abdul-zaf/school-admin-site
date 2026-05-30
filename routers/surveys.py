from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from database import get_db
import models
import security

router = APIRouter()


class SurveyQuestionIn(BaseModel):
    question_text: str
    question_type: str  # text, multiple_choice, rating
    options: Optional[Any] = None
    order_num: int = 0


class SurveyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_anonymous: bool = False
    due_date: Optional[datetime] = None
    questions: List[SurveyQuestionIn] = []


class SurveyAnswerIn(BaseModel):
    question_id: int
    answer_text: str


class SurveyResponseIn(BaseModel):
    answers: List[SurveyAnswerIn]


@router.get("/course/{course_id}")
def list_surveys(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    surveys = db.query(models.Survey).filter(models.Survey.course_id == course_id).all()
    result = []
    for s in surveys:
        # Check if student already responded
        already_responded = False
        if current_user.role == "student":
            already_responded = db.query(models.SurveyResponse).filter(
                models.SurveyResponse.survey_id == s.id,
                models.SurveyResponse.student_id == current_user.id,
            ).first() is not None
        result.append({
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "is_anonymous": s.is_anonymous,
            "due_date": str(s.due_date) if s.due_date else None,
            "question_count": len(s.questions),
            "response_count": len(s.responses),
            "already_responded": already_responded,
        })
    return result


@router.post("/course/{course_id}")
def create_survey(
    course_id: int,
    data: SurveyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    survey = models.Survey(
        course_id=course_id,
        title=data.title,
        description=data.description,
        is_anonymous=data.is_anonymous,
        due_date=data.due_date,
    )
    db.add(survey)
    db.flush()

    for i, q_data in enumerate(data.questions):
        q = models.SurveyQuestion(
            survey_id=survey.id,
            question_text=q_data.question_text,
            question_type=q_data.question_type,
            options=q_data.options,
            order_num=q_data.order_num if q_data.order_num else i,
        )
        db.add(q)

    db.commit()
    db.refresh(survey)
    return {"id": survey.id, "title": survey.title}


@router.get("/{survey_id}")
def get_survey(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    survey = db.query(models.Survey).filter(models.Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(404, "Survey not found")
    return {
        "id": survey.id,
        "title": survey.title,
        "description": survey.description,
        "is_anonymous": survey.is_anonymous,
        "due_date": str(survey.due_date) if survey.due_date else None,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "options": q.options,
                "order_num": q.order_num,
            }
            for q in survey.questions
        ],
    }


@router.delete("/{survey_id}")
def delete_survey(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    survey = db.query(models.Survey).filter(models.Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(404, "Survey not found")
    security.require_course_access(survey.course_id, current_user, db)
    db.delete(survey)
    db.commit()
    return {"ok": True}


@router.post("/{survey_id}/respond")
def submit_response(
    survey_id: int,
    data: SurveyResponseIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    survey = db.query(models.Survey).filter(models.Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(404, "Survey not found")

    # Check if already responded (non-anonymous)
    if not survey.is_anonymous:
        existing = db.query(models.SurveyResponse).filter(
            models.SurveyResponse.survey_id == survey_id,
            models.SurveyResponse.student_id == current_user.id,
        ).first()
        if existing:
            raise HTTPException(400, "Already responded to this survey")

    student_id = None if survey.is_anonymous else current_user.id
    response = models.SurveyResponse(
        survey_id=survey_id,
        student_id=student_id,
    )
    db.add(response)
    db.flush()

    for ans_data in data.answers:
        ans = models.SurveyAnswer(
            response_id=response.id,
            question_id=ans_data.question_id,
            answer_text=ans_data.answer_text,
        )
        db.add(ans)

    db.commit()
    return {"ok": True, "response_id": response.id}


@router.get("/{survey_id}/results")
def survey_results(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    survey = db.query(models.Survey).filter(models.Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(404, "Survey not found")
    security.require_course_access(survey.course_id, current_user, db)

    results = []
    for q in survey.questions:
        answers = db.query(models.SurveyAnswer).filter(
            models.SurveyAnswer.question_id == q.id
        ).all()
        answer_texts = [a.answer_text for a in answers]

        # Aggregate for multiple choice
        if q.question_type == "multiple_choice" and q.options:
            tally = {}
            for opt in q.options:
                opt_text = opt if isinstance(opt, str) else opt.get("text", str(opt))
                tally[opt_text] = 0
            for ans in answer_texts:
                if ans in tally:
                    tally[ans] += 1
        elif q.question_type == "rating":
            nums = [float(a) for a in answer_texts if a and a.replace('.', '').isdigit()]
            tally = {"avg": round(sum(nums) / len(nums), 2) if nums else 0, "count": len(nums)}
        else:
            tally = {"responses": answer_texts}

        results.append({
            "question_id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "response_count": len(answers),
            "summary": tally,
        })

    return {
        "survey_id": survey_id,
        "title": survey.title,
        "total_responses": len(survey.responses),
        "questions": results,
    }
