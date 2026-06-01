"""
Leaderboard — ranks students by average grade.

GET /api/leaderboard/course/{course_id}
  • Teachers / admins : full names
  • Students          : own name shown; others shown as "Student #N"

GET /api/leaderboard/school   (admin only)
  • Top 25 students school-wide by cumulative average
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import security

router = APIRouter()


def _course_scores(course_id: int, db: Session) -> list[dict]:
    """Return [{student_id, name, avg_pct}] sorted best-first."""
    enrollments = (
        db.query(models.Enrollment)
        .filter(models.Enrollment.course_id == course_id)
        .all()
    )
    rows = []
    for e in enrollments:
        sid    = e.student_id
        scores, totals = [], []

        subs = (
            db.query(models.Submission)
            .join(models.Assignment)
            .filter(
                models.Submission.student_id  == sid,
                models.Assignment.course_id   == course_id,
                models.Submission.score       != None,   # noqa: E711
            )
            .all()
        )
        for s in subs:
            if s.assignment.max_score:
                scores.append(s.score)
                totals.append(s.assignment.max_score)

        attempts = (
            db.query(models.QuizAttempt)
            .join(models.Quiz)
            .filter(
                models.QuizAttempt.student_id  == sid,
                models.Quiz.course_id          == course_id,
                models.QuizAttempt.score       != None,   # noqa: E711
            )
            .all()
        )
        for a in attempts:
            total_pts = sum(q.points for q in a.quiz.questions)
            if total_pts:
                scores.append(a.score)
                totals.append(total_pts)

        avg = (
            sum(scores[i] / totals[i] * 100 for i in range(len(scores)))
            / len(scores)
            if scores else 0.0
        )
        rows.append({"student_id": sid, "name": e.student.name, "avg_pct": round(avg, 1)})

    rows.sort(key=lambda r: r["avg_pct"], reverse=True)
    return rows


@router.get("/course/{course_id}")
def course_leaderboard(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")

    is_teacher = (
        current_user.role == "admin"
        or (current_user.role == "teacher" and course.teacher_id == current_user.id)
    )

    rows = _course_scores(course_id, db)

    result = []
    for i, row in enumerate(rows, 1):
        is_me  = row["student_id"] == current_user.id
        # Students see real names only for themselves; others are anonymised
        name   = row["name"] if (is_teacher or is_me) else f"Student #{i}"
        result.append({
            "rank":    i,
            "name":    name,
            "avg_pct": row["avg_pct"],
            "is_me":   is_me,
        })

    return {"course_title": course.title, "entries": result}


@router.get("/school")
def school_leaderboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """School-wide top 25 — admin / teacher only."""
    students = db.query(models.User).filter(models.User.role == "student").all()
    rows = []
    for s in students:
        scores, totals = [], []
        for sub in s.submissions:
            if sub.score is not None and sub.assignment.max_score:
                scores.append(sub.score)
                totals.append(sub.assignment.max_score)
        for att in s.quiz_attempts:
            if att.score is not None:
                total_pts = sum(q.points for q in att.quiz.questions)
                if total_pts:
                    scores.append(att.score)
                    totals.append(total_pts)
        avg = (
            sum(scores[i] / totals[i] * 100 for i in range(len(scores)))
            / len(scores)
            if scores else 0.0
        )
        if scores:  # only include students with at least one grade
            rows.append({"name": s.name, "avg_pct": round(avg, 1)})

    rows.sort(key=lambda r: r["avg_pct"], reverse=True)
    return {"entries": [{"rank": i + 1, **r} for i, r in enumerate(rows[:25])]}
