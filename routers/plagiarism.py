"""
plagiarism.py — Content-fingerprinting plagiarism detection.

POST /api/plagiarism/check/{assignment_id}  Run check on all submissions (teacher/admin)
GET  /api/plagiarism/{assignment_id}        Get existing reports for an assignment (teacher/admin)
"""
import difflib
import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
import security

router = APIRouter()

SIMILARITY_THRESHOLD = 0.80


def _normalize(text: str) -> str:
    """Normalize text for comparison: lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _similarity(a: str, b: str) -> float:
    na, nb = _normalize(a), _normalize(b)
    if not na or not nb:
        return 0.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


@router.post("/check/{assignment_id}")
def run_plagiarism_check(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(404, "Assignment not found")
    security.require_course_access(assignment.course_id, current_user, db)

    submissions = db.query(models.Submission).filter(
        models.Submission.assignment_id == assignment_id,
        models.Submission.content != None,
    ).all()

    if len(submissions) < 2:
        return {"message": "Need at least 2 submissions to check for plagiarism", "reports": []}

    now = datetime.utcnow()
    reports = []
    for i in range(len(submissions)):
        for j in range(i + 1, len(submissions)):
            sub_a = submissions[i]
            sub_b = submissions[j]
            score = _similarity(sub_a.content or "", sub_b.content or "")
            # Upsert report
            existing = db.query(models.PlagiarismReport).filter(
                models.PlagiarismReport.assignment_id == assignment_id,
                models.PlagiarismReport.submission_a_id == sub_a.id,
                models.PlagiarismReport.submission_b_id == sub_b.id,
            ).first()
            if existing:
                existing.similarity_score = score
                existing.checked_at = now
                report = existing
            else:
                report = models.PlagiarismReport(
                    assignment_id=assignment_id,
                    submission_a_id=sub_a.id,
                    submission_b_id=sub_b.id,
                    similarity_score=score,
                    checked_at=now,
                )
                db.add(report)
            reports.append({
                "submission_a_id": sub_a.id,
                "student_a": sub_a.student.name if sub_a.student else str(sub_a.student_id),
                "submission_b_id": sub_b.id,
                "student_b": sub_b.student.name if sub_b.student else str(sub_b.student_id),
                "similarity_score": round(score, 4),
                "flagged": score >= SIMILARITY_THRESHOLD,
            })
    db.commit()
    flagged = [r for r in reports if r["flagged"]]
    return {
        "total_pairs": len(reports),
        "flagged_pairs": len(flagged),
        "threshold": SIMILARITY_THRESHOLD,
        "reports": sorted(reports, key=lambda x: x["similarity_score"], reverse=True),
    }


@router.get("/{assignment_id}")
def get_reports(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(404, "Assignment not found")
    security.require_course_access(assignment.course_id, current_user, db)

    rpts = db.query(models.PlagiarismReport).filter(
        models.PlagiarismReport.assignment_id == assignment_id
    ).order_by(models.PlagiarismReport.similarity_score.desc()).all()

    return [
        {
            "id": r.id,
            "submission_a_id": r.submission_a_id,
            "student_a": r.submission_a.student.name if r.submission_a and r.submission_a.student else None,
            "submission_b_id": r.submission_b_id,
            "student_b": r.submission_b.student.name if r.submission_b and r.submission_b.student else None,
            "similarity_score": r.similarity_score,
            "flagged": r.similarity_score >= SIMILARITY_THRESHOLD,
            "checked_at": str(r.checked_at),
        }
        for r in rpts
    ]
