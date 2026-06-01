"""
Completion certificates — generated as PDF with ReportLab.

A student is eligible when they have:
  • Submitted every assignment in the course
  • Attempted every published quiz in the course
  • Achieved an average grade of at least 50 %
"""
from datetime import datetime
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
import models
import security

router = APIRouter()


def _pct(score, max_score) -> float:
    return round(score / max_score * 100, 1) if max_score else 0.0


def _eligibility(student_id: int, course_id: int, db: Session):
    """
    Returns (eligible: bool, reason: str, avg_pct: float).
    """
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        return False, "Course not found", 0.0

    assignments = db.query(models.Assignment).filter(
        models.Assignment.course_id == course_id
    ).all()

    quizzes = db.query(models.Quiz).filter(
        models.Quiz.course_id    == course_id,
        models.Quiz.is_published == True,           # noqa: E712
    ).all()

    scores, totals = [], []

    # Check assignments
    for a in assignments:
        sub = db.query(models.Submission).filter(
            models.Submission.assignment_id == a.id,
            models.Submission.student_id    == student_id,
        ).first()
        if not sub:
            return False, f"Assignment '{a.title}' not yet submitted.", 0.0
        if sub.score is not None:
            scores.append(sub.score)
            totals.append(a.max_score)

    # Check quizzes
    for q in quizzes:
        attempt = db.query(models.QuizAttempt).filter(
            models.QuizAttempt.quiz_id     == q.id,
            models.QuizAttempt.student_id  == student_id,
            models.QuizAttempt.submitted_at != None,   # noqa: E711
        ).first()
        if not attempt:
            return False, f"Quiz '{q.title}' not yet completed.", 0.0
        if attempt.score is not None:
            total_pts = sum(qq.points for qq in q.questions)
            scores.append(attempt.score)
            totals.append(total_pts)

    if not assignments and not quizzes:
        return False, "This course has no assessments yet.", 0.0

    avg_pct = (
        sum(scores[i] / totals[i] * 100 for i in range(len(scores)) if totals[i])
        / len(scores)
        if scores else 0.0
    )
    if avg_pct < 50:
        return False, f"Average grade is {avg_pct:.1f}% — minimum 50% required.", avg_pct

    return True, "Eligible", round(avg_pct, 1)


def _build_pdf(
    student_name: str,
    course_title: str,
    teacher_name: str,
    grade_pct: float,
    issue_date: str,
) -> BytesIO:
    """Generate and return a landscape-A4 certificate as a BytesIO PDF."""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.colors import HexColor
    from reportlab.pdfgen import canvas as rl_canvas

    buf = BytesIO()
    W, H = landscape(A4)
    c = rl_canvas.Canvas(buf, pagesize=landscape(A4))

    # ── Dark indigo background ──
    c.setFillColor(HexColor("#1e1b4b"))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── Gold outer border ──
    c.setStrokeColor(HexColor("#f59e0b"))
    c.setLineWidth(6)
    c.rect(18, 18, W - 36, H - 36, fill=0)

    # ── White inner panel ──
    c.setFillColor(HexColor("#ffffff"))
    c.rect(30, 30, W - 60, H - 60, fill=1, stroke=0)

    # ── Indigo accent bar at top of panel ──
    c.setFillColor(HexColor("#4f46e5"))
    c.rect(30, H - 100, W - 60, 70, fill=1, stroke=0)

    # ── "EduPortal" on the bar ──
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, H - 70, "EduPortal — School Learning Management System")

    # ── Main heading ──
    c.setFillColor(HexColor("#1e1b4b"))
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(W / 2, H - 148, "Certificate of Completion")

    # ── Gold divider ──
    c.setStrokeColor(HexColor("#f59e0b"))
    c.setLineWidth(2)
    c.line(120, H - 162, W - 120, H - 162)

    # ── "This certifies that" ──
    c.setFillColor(HexColor("#6b7280"))
    c.setFont("Helvetica", 15)
    c.drawCentredString(W / 2, H - 200, "This is to certify that")

    # ── Student name ──
    c.setFillColor(HexColor("#1e1b4b"))
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 258, student_name)

    # ── "has successfully completed" ──
    c.setFillColor(HexColor("#6b7280"))
    c.setFont("Helvetica", 15)
    c.drawCentredString(W / 2, H - 292, "has successfully completed the course")

    # ── Course title ──
    c.setFillColor(HexColor("#4f46e5"))
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(W / 2, H - 340, course_title)

    # ── Grade ──
    grade_color = (
        HexColor("#059669") if grade_pct >= 80
        else HexColor("#d97706") if grade_pct >= 60
        else HexColor("#e11d48")
    )
    c.setFillColor(grade_color)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(W / 2, H - 378, f"with an overall grade of  {grade_pct}%")

    # ── Issue date ──
    c.setFillColor(HexColor("#6b7280"))
    c.setFont("Helvetica", 13)
    c.drawCentredString(W / 2, H - 412, f"Issued on  {issue_date}")

    # ── Gold divider ──
    c.setStrokeColor(HexColor("#f59e0b"))
    c.setLineWidth(1.5)
    c.line(160, H - 435, W - 160, H - 435)

    # ── Signature line ──
    c.setStrokeColor(HexColor("#1e1b4b"))
    c.setLineWidth(1)
    sig_x = W / 2
    c.line(sig_x - 110, H - 472, sig_x + 110, H - 472)
    c.setFillColor(HexColor("#374151"))
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(sig_x, H - 486, teacher_name)
    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor("#6b7280"))
    c.drawCentredString(sig_x, H - 500, "Course Teacher")

    c.save()
    buf.seek(0)
    return buf


# ── Endpoint ──────────────────────────────────────────────────────────────────

@router.get("/course/{course_id}")
def download_certificate(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    # Must be enrolled
    enrolment = db.query(models.Enrollment).filter(
        models.Enrollment.course_id  == course_id,
        models.Enrollment.student_id == current_user.id,
    ).first()
    if not enrolment:
        raise HTTPException(403, "You are not enrolled in this course.")

    eligible, reason, avg_pct = _eligibility(current_user.id, course_id, db)
    if not eligible:
        raise HTTPException(403, reason)

    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    teacher_name = course.teacher.name if course.teacher else "EduPortal"
    # %-d (no-zero-pad day) is Linux-only; strip manually for cross-platform
    _now = datetime.utcnow()
    issue_date = f"{_now.day} {_now.strftime('%B %Y')}"

    try:
        pdf_buf = _build_pdf(
            student_name = current_user.name,
            course_title = course.title,
            teacher_name = teacher_name,
            grade_pct    = avg_pct,
            issue_date   = issue_date,
        )
    except ImportError:
        raise HTTPException(500, "PDF generation library (reportlab) not installed.")

    filename = f"certificate_{course.title.replace(' ', '_')}.pdf"
    return StreamingResponse(
        pdf_buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/course/{course_id}/check")
def check_certificate_eligibility(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    """Returns eligibility without generating the PDF — used by the frontend."""
    enrolment = db.query(models.Enrollment).filter(
        models.Enrollment.course_id  == course_id,
        models.Enrollment.student_id == current_user.id,
    ).first()
    if not enrolment:
        return {"eligible": False, "reason": "Not enrolled."}

    eligible, reason, avg_pct = _eligibility(current_user.id, course_id, db)
    return {"eligible": eligible, "reason": reason, "avg_pct": avg_pct}
