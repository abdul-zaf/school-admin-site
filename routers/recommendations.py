"""
recommendations.py — Content recommendations based on quiz performance.

GET  /api/recommendations/my                    Personalized recommendations (student)
POST /api/recommendations/{id}/dismiss          Dismiss a recommendation (student)
POST /api/recommendations/generate/{course_id}  Regenerate for all students (teacher/admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
import security

router = APIRouter()


def _generate_for_student(db: Session, student_id: int, course_id: int):
    """Generate recommendations for one student in one course."""
    # Get quiz attempts for this student in this course
    quizzes = db.query(models.Quiz).filter(models.Quiz.course_id == course_id).all()
    quiz_ids = [q.id for q in quizzes]
    if not quiz_ids:
        return

    attempts = db.query(models.QuizAttempt).filter(
        models.QuizAttempt.student_id == student_id,
        models.QuizAttempt.quiz_id.in_(quiz_ids),
        models.QuizAttempt.submitted_at != None,
        models.QuizAttempt.score != None,
    ).all()

    if not attempts:
        return

    # Find the attempt with lowest score relative to total possible
    worst_attempts = []
    for attempt in attempts:
        quiz = next((q for q in quizzes if q.id == attempt.quiz_id), None)
        if quiz:
            total_pts = sum(qq.points for qq in quiz.questions)
            if total_pts > 0:
                pct = attempt.score / total_pts * 100
                worst_attempts.append((pct, quiz, attempt))

    if not worst_attempts:
        return

    worst_attempts.sort(key=lambda x: x[0])
    trigger_pct, worst_quiz, worst_attempt = worst_attempts[0]

    if trigger_pct >= 70:
        return  # Student is doing fine, no recommendation needed

    # Find materials related to the weak quiz
    materials = db.query(models.Material).filter(
        models.Material.course_id == course_id
    ).all()

    # Clear old undismissed recommendations for this student/course
    db.query(models.Recommendation).filter(
        models.Recommendation.student_id == student_id,
        models.Recommendation.course_id == course_id,
        models.Recommendation.is_dismissed == False,
    ).delete()

    if materials:
        # Recommend the first matching material
        mat = materials[0]
        rec = models.Recommendation(
            student_id=student_id,
            course_id=course_id,
            material_id=mat.id,
            reason=(
                f"Your score on '{worst_quiz.title}' was {trigger_pct:.0f}%. "
                f"Review '{mat.title}' to strengthen your understanding."
            ),
            score_trigger=trigger_pct,
        )
        db.add(rec)
    else:
        rec = models.Recommendation(
            student_id=student_id,
            course_id=course_id,
            material_id=None,
            reason=(
                f"Your score on '{worst_quiz.title}' was {trigger_pct:.0f}%. "
                f"We recommend reviewing the course materials for this topic."
            ),
            score_trigger=trigger_pct,
        )
        db.add(rec)


@router.get("/my")
def my_recommendations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    # Auto-generate if none exist
    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == current_user.id
    ).all()
    for enr in enrollments:
        existing = db.query(models.Recommendation).filter(
            models.Recommendation.student_id == current_user.id,
            models.Recommendation.course_id == enr.course_id,
            models.Recommendation.is_dismissed == False,
        ).first()
        if not existing:
            _generate_for_student(db, current_user.id, enr.course_id)
    db.commit()

    recs = db.query(models.Recommendation).filter(
        models.Recommendation.student_id == current_user.id,
        models.Recommendation.is_dismissed == False,
    ).order_by(models.Recommendation.score_trigger).all()

    return [
        {
            "id": r.id,
            "course_id": r.course_id,
            "course_title": r.course.title if r.course else None,
            "material_id": r.material_id,
            "material_title": r.material.title if r.material else None,
            "reason": r.reason,
            "score_trigger": r.score_trigger,
            "created_at": str(r.created_at),
        }
        for r in recs
    ]


@router.post("/{rec_id}/dismiss")
def dismiss_recommendation(
    rec_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    rec = db.query(models.Recommendation).filter(
        models.Recommendation.id == rec_id,
        models.Recommendation.student_id == current_user.id,
    ).first()
    if not rec:
        raise HTTPException(404, "Recommendation not found")
    rec.is_dismissed = True
    db.commit()
    return {"ok": True}


@router.post("/generate/{course_id}")
def generate_recommendations(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    security.require_course_access(course_id, current_user, db)

    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course_id
    ).all()
    count = 0
    for enr in enrollments:
        _generate_for_student(db, enr.student_id, course_id)
        count += 1
    db.commit()
    return {"generated_for": count, "course_id": course_id}
