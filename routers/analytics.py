from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
import models
import security
from routers.gradebook import score_to_letter, compute_weighted_grade

router = APIRouter()


@router.get("/course/{course_id}")
def course_analytics(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")

    enrollments = db.query(models.Enrollment).filter(models.Enrollment.course_id == course_id).all()
    student_ids = [e.student_id for e in enrollments]
    assignments = db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()
    categories = db.query(models.GradeCategory).filter(models.GradeCategory.course_id == course_id).all()

    assignment_stats = []
    grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    active_students = set()

    for a in assignments:
        subs = db.query(models.Submission).filter(
            models.Submission.assignment_id == a.id
        ).all()
        graded = [s for s in subs if s.score is not None]
        avg = sum(s.score for s in graded) / len(graded) if graded else 0
        active_students.update(s.student_id for s in subs)
        assignment_stats.append({
            "assignment_id": a.id,
            "title": a.title,
            "submission_count": len(subs),
            "enrollment_count": len(student_ids),
            "submission_rate": round(len(subs) / len(student_ids) * 100, 1) if student_ids else 0,
            "graded_count": len(graded),
            "avg_score": round(avg, 2),
            "avg_pct": round(avg / a.max_score * 100, 1) if a.max_score else 0,
        })

    # Grade distribution per student
    for sid in student_ids:
        subs = db.query(models.Submission).filter(
            models.Submission.student_id == sid,
            models.Submission.assignment_id.in_([a.id for a in assignments]),
        ).all()
        sub_map = {s.assignment_id: s for s in subs}
        grade_info = compute_weighted_grade(sid, assignments, sub_map, categories)
        grade_dist[grade_info["letter"]] += 1

    return {
        "course_id": course_id,
        "course_title": course.title,
        "enrollment_count": len(student_ids),
        "active_students": len(active_students),
        "assignment_stats": assignment_stats,
        "grade_distribution": grade_dist,
    }


@router.get("/overview")
def admin_overview(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    total_users = db.query(models.User).count()
    total_courses = db.query(models.Course).count()
    total_students = db.query(models.User).filter(models.User.role == "student").count()
    total_teachers = db.query(models.User).filter(models.User.role == "teacher").count()
    total_enrollments = db.query(models.Enrollment).count()

    week_ago = datetime.utcnow() - timedelta(days=7)
    submissions_this_week = db.query(models.Submission).filter(
        models.Submission.submitted_at >= week_ago
    ).count()

    graded_subs = db.query(models.Submission).filter(models.Submission.score != None).all()
    avg_grade = 0.0
    if graded_subs:
        pcts = []
        for s in graded_subs:
            if s.assignment and s.assignment.max_score:
                pcts.append(s.score / s.assignment.max_score * 100)
        avg_grade = round(sum(pcts) / len(pcts), 1) if pcts else 0.0

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "submissions_this_week": submissions_this_week,
        "avg_grade_pct": avg_grade,
    }


@router.get("/my")
def my_analytics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == current_user.id
    ).all()

    courses_data = []
    for enr in enrollments:
        course = enr.course
        assignments = db.query(models.Assignment).filter(
            models.Assignment.course_id == course.id
        ).all()
        categories = db.query(models.GradeCategory).filter(
            models.GradeCategory.course_id == course.id
        ).all()
        subs = db.query(models.Submission).filter(
            models.Submission.student_id == current_user.id,
            models.Submission.assignment_id.in_([a.id for a in assignments]),
        ).all()
        sub_map = {s.assignment_id: s for s in subs}

        submitted_count = len(subs)
        total_assignments = len([a for a in assignments if not a.is_extra_credit])
        completion_pct = int(submitted_count / total_assignments * 100) if total_assignments else 100

        grade_info = compute_weighted_grade(current_user.id, assignments, sub_map, categories)
        courses_data.append({
            "course_id": course.id,
            "course_title": course.title,
            "total_assignments": total_assignments,
            "submitted_count": submitted_count,
            "completion_pct": completion_pct,
            **grade_info,
        })

    return {"courses": courses_data}
