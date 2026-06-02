"""
analytics.py — Aggregate statistics for teachers and admins.

GET /api/analytics/course/{id}                  Per-course stats
GET /api/analytics/overview                     School-wide summary (admin)
GET /api/analytics/my                           Student's own analytics
GET /api/analytics/at-risk                      At-risk students (teacher/admin)
GET /api/analytics/teacher-performance          Per-teacher metrics (admin)
GET /api/analytics/course-effectiveness/{id}   Course effectiveness (teacher/admin)
GET /api/analytics/export/gradebook/{id}        CSV gradebook export (teacher/admin)
GET /api/analytics/export/attendance/{id}       CSV attendance export (teacher/admin)
GET /api/analytics/export/transcript/{id}       PDF transcript (admin)
"""
import io
import csv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
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


@router.get("/at-risk")
def at_risk_students(
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Students with <60% avg grade OR <50% submission rate OR <70% attendance."""
    if course_id:
        security.require_course_access(course_id, current_user, db)
        enrollments = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == course_id
        ).all()
    else:
        if current_user.role == "teacher":
            # Teacher sees their own courses
            teacher_courses = db.query(models.Course).filter(
                models.Course.teacher_id == current_user.id
            ).all()
            course_ids = [c.id for c in teacher_courses]
            enrollments = db.query(models.Enrollment).filter(
                models.Enrollment.course_id.in_(course_ids)
            ).all()
        else:
            enrollments = db.query(models.Enrollment).all()

    at_risk = []
    seen_students = set()
    for enr in enrollments:
        if enr.student_id in seen_students:
            continue
        seen_students.add(enr.student_id)

        student = db.query(models.User).filter(models.User.id == enr.student_id).first()
        if not student:
            continue

        risk_factors = []
        cid = enr.course_id
        assignments = db.query(models.Assignment).filter(models.Assignment.course_id == cid).all()
        subs = db.query(models.Submission).filter(
            models.Submission.student_id == enr.student_id,
            models.Submission.assignment_id.in_([a.id for a in assignments]),
        ).all()

        # Submission rate
        if assignments:
            sub_rate = len(subs) / len(assignments) * 100
            if sub_rate < 50:
                risk_factors.append(f"Low submission rate: {sub_rate:.0f}%")

        # Average grade
        graded = [s for s in subs if s.score is not None]
        if graded:
            pcts = [s.score / s.assignment.max_score * 100 for s in graded if s.assignment and s.assignment.max_score]
            if pcts:
                avg_pct = sum(pcts) / len(pcts)
                if avg_pct < 60:
                    risk_factors.append(f"Low average grade: {avg_pct:.0f}%")

        # Attendance
        att_records = db.query(models.Attendance).filter(
            models.Attendance.course_id == cid,
            models.Attendance.student_id == enr.student_id,
        ).all()
        if att_records:
            present = sum(1 for a in att_records if a.status == "present")
            att_rate = present / len(att_records) * 100
            if att_rate < 70:
                risk_factors.append(f"Low attendance: {att_rate:.0f}%")

        if risk_factors:
            at_risk.append({
                "student_id": student.id,
                "student_name": student.name,
                "student_email": student.email,
                "course_id": cid,
                "risk_factors": risk_factors,
            })

    return {"at_risk_students": at_risk, "total": len(at_risk)}


@router.get("/teacher-performance")
def teacher_performance(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    """Per-teacher metrics: avg course rating, avg student grade, enrollment count, submission rate."""
    teachers = db.query(models.User).filter(models.User.role == "teacher").all()
    results = []
    for teacher in teachers:
        courses = db.query(models.Course).filter(models.Course.teacher_id == teacher.id).all()
        course_ids = [c.id for c in courses]
        total_enrolled = db.query(models.Enrollment).filter(
            models.Enrollment.course_id.in_(course_ids)
        ).count() if course_ids else 0

        # Avg rating
        ratings = db.query(models.CourseRating).filter(
            models.CourseRating.course_id.in_(course_ids)
        ).all() if course_ids else []
        avg_rating = round(sum(r.rating for r in ratings) / len(ratings), 2) if ratings else None

        # Avg grade & submission rate
        assignments = db.query(models.Assignment).filter(
            models.Assignment.course_id.in_(course_ids)
        ).all() if course_ids else []
        subs = db.query(models.Submission).filter(
            models.Submission.assignment_id.in_([a.id for a in assignments])
        ).all() if assignments else []
        graded = [s for s in subs if s.score is not None]
        pcts = [s.score / s.assignment.max_score * 100 for s in graded if s.assignment and s.assignment.max_score]
        avg_grade = round(sum(pcts) / len(pcts), 1) if pcts else None
        sub_rate = round(len(subs) / (len(assignments) * total_enrolled) * 100, 1) if assignments and total_enrolled else None

        results.append({
            "teacher_id": teacher.id,
            "teacher_name": teacher.name,
            "course_count": len(courses),
            "total_enrolled": total_enrolled,
            "avg_course_rating": avg_rating,
            "avg_student_grade_pct": avg_grade,
            "submission_rate_pct": sub_rate,
        })

    return results


@router.get("/course-effectiveness/{course_id}")
def course_effectiveness(
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

    # Module completion rate
    modules = db.query(models.CourseModule).filter(models.CourseModule.course_id == course_id).all()
    all_items = [item for mod in modules for item in mod.items if item.is_required]
    completed_total = 0
    if all_items and student_ids:
        for item in all_items:
            completed_total += db.query(models.ModuleCompletion).filter(
                models.ModuleCompletion.module_item_id == item.id,
                models.ModuleCompletion.student_id.in_(student_ids),
            ).count()
        completion_rate = completed_total / (len(all_items) * len(student_ids)) * 100 if student_ids else 0
    else:
        completion_rate = 0

    # Quiz score improvement (first vs last quiz per student)
    quizzes = db.query(models.Quiz).filter(models.Quiz.course_id == course_id).order_by(models.Quiz.created_at).all()
    improvements = []
    if len(quizzes) >= 2:
        for sid in student_ids:
            first_att = db.query(models.QuizAttempt).filter(
                models.QuizAttempt.quiz_id == quizzes[0].id,
                models.QuizAttempt.student_id == sid,
                models.QuizAttempt.score != None,
            ).first()
            last_att = db.query(models.QuizAttempt).filter(
                models.QuizAttempt.quiz_id == quizzes[-1].id,
                models.QuizAttempt.student_id == sid,
                models.QuizAttempt.score != None,
            ).first()
            if first_att and last_att:
                first_pts = sum(q.points for q in quizzes[0].questions) or 1
                last_pts = sum(q.points for q in quizzes[-1].questions) or 1
                improvement = (last_att.score / last_pts - first_att.score / first_pts) * 100
                improvements.append(improvement)
    avg_improvement = round(sum(improvements) / len(improvements), 1) if improvements else None

    # Dropout rate: students with no recent activity (no submission in last 30 days)
    recent = datetime.utcnow() - timedelta(days=30)
    assignments = db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()
    active_students = set()
    for a in assignments:
        subs = db.query(models.Submission).filter(
            models.Submission.assignment_id == a.id,
            models.Submission.submitted_at >= recent,
        ).all()
        active_students.update(s.student_id for s in subs)
    dropout_rate = round((len(student_ids) - len(active_students)) / len(student_ids) * 100, 1) if student_ids else 0

    return {
        "course_id": course_id,
        "course_title": course.title,
        "enrollment_count": len(student_ids),
        "module_completion_rate_pct": round(completion_rate, 1),
        "avg_quiz_score_improvement_pct": avg_improvement,
        "dropout_rate_pct": dropout_rate,
        "active_last_30d": len(active_students),
    }


@router.get("/export/gradebook/{course_id}")
def export_gradebook_csv(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")

    enrollments = db.query(models.Enrollment).filter(models.Enrollment.course_id == course_id).all()
    assignments = db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    # Header
    header = ["Student ID", "Student Name", "Email"] + [a.title for a in assignments] + ["Average %"]
    writer.writerow(header)

    for enr in enrollments:
        student = enr.student
        row = [student.id, student.name, student.email]
        scores = []
        for a in assignments:
            sub = db.query(models.Submission).filter(
                models.Submission.assignment_id == a.id,
                models.Submission.student_id == student.id,
            ).first()
            if sub and sub.score is not None:
                pct = round(sub.score / a.max_score * 100, 1) if a.max_score else 0
                row.append(f"{sub.score}/{a.max_score} ({pct}%)")
                scores.append(pct)
            else:
                row.append("Not submitted")
        avg = round(sum(scores) / len(scores), 1) if scores else 0
        row.append(f"{avg}%")
        writer.writerow(row)

    output.seek(0)
    filename = f"gradebook_{course.title.replace(' ', '_')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/export/attendance/{course_id}")
def export_attendance_csv(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    security.require_course_access(course_id, current_user, db)
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")

    records = db.query(models.Attendance).filter(
        models.Attendance.course_id == course_id
    ).order_by(models.Attendance.date).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student ID", "Student Name", "Date", "Status"])
    for r in records:
        student = db.query(models.User).filter(models.User.id == r.student_id).first()
        writer.writerow([
            r.student_id,
            student.name if student else "Unknown",
            str(r.date),
            r.status,
        ])

    output.seek(0)
    filename = f"attendance_{course.title.replace(' ', '_')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/export/transcript/{student_id}")
def export_transcript_pdf(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    student = db.query(models.User).filter(models.User.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
    except ImportError:
        raise HTTPException(503, "reportlab not installed")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Official Academic Transcript", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Student: {student.name}", styles["Heading2"]))
    story.append(Paragraph(f"Email: {student.email}", styles["Normal"]))
    story.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d')}", styles["Normal"]))
    story.append(Spacer(1, 20))

    enrollments = db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id).all()
    for enr in enrollments:
        course = enr.course
        story.append(Paragraph(f"Course: {course.title}", styles["Heading3"]))
        assignments = db.query(models.Assignment).filter(models.Assignment.course_id == course.id).all()
        table_data = [["Assignment", "Score", "Max", "Grade %"]]
        for a in assignments:
            sub = db.query(models.Submission).filter(
                models.Submission.assignment_id == a.id,
                models.Submission.student_id == student_id,
            ).first()
            if sub and sub.score is not None:
                pct = round(sub.score / a.max_score * 100, 1) if a.max_score else 0
                table_data.append([a.title, str(sub.score), str(a.max_score), f"{pct}%"])
            else:
                table_data.append([a.title, "N/A", str(a.max_score), "-"])
        if len(table_data) > 1:
            t = Table(table_data)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]))
            story.append(t)
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    filename = f"transcript_{student.name.replace(' ', '_')}.pdf"
    return StreamingResponse(
        iter([buffer.read()]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
