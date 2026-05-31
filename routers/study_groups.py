"""
Study group auto-matcher.

Students can self-organise into groups, OR teachers can trigger auto-matching
which uses quiz/assignment performance to create groups with complementary strengths.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database import get_db
import models
import security

router = APIRouter()


class GroupCreate(BaseModel):
    name: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _student_score(student_id: int, course_id: int, db: Session) -> float:
    """Weighted average of quiz + assignment scores for one student in one course."""
    quiz_scores = [
        a.score
        for a in db.query(models.QuizAttempt)
        .join(models.Quiz)
        .filter(
            models.QuizAttempt.student_id == student_id,
            models.Quiz.course_id         == course_id,
            models.QuizAttempt.score      != None,
        )
        .all()
    ]
    sub_scores = [
        s.score
        for s in db.query(models.Submission)
        .join(models.Assignment)
        .filter(
            models.Submission.student_id  == student_id,
            models.Assignment.course_id   == course_id,
            models.Submission.score       != None,
        )
        .all()
    ]
    all_scores = quiz_scores + sub_scores
    return sum(all_scores) / len(all_scores) if all_scores else 50.0


def _auto_match(course_id: int, group_size: int, db: Session):
    """
    Sort enrolled students by overall score, then interleave them so each group
    mixes a high, middle, and low performer (complementary strengths).
    """
    enrollments = (
        db.query(models.Enrollment)
        .filter(models.Enrollment.course_id == course_id)
        .all()
    )
    student_ids = [e.student_id for e in enrollments]
    if not student_ids:
        return []

    scored = sorted(
        student_ids,
        key=lambda sid: _student_score(sid, course_id, db),
    )

    # Interleave: group i gets students at positions i, i+n, i+2n, …
    n = max(1, len(scored) // group_size)
    groups = [[] for _ in range(n)]
    for idx, sid in enumerate(scored):
        groups[idx % n].append(sid)

    return [g for g in groups if g]


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/course/{course_id}")
def list_groups(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    groups = (
        db.query(models.StudyGroup)
        .filter(models.StudyGroup.course_id == course_id)
        .all()
    )
    my_group_ids = set()
    if current_user.role == "student":
        my_group_ids = {
            m.group_id
            for m in db.query(models.StudyGroupMember)
            .filter(models.StudyGroupMember.student_id == current_user.id)
            .all()
        }

    return [
        {
            "id":              g.id,
            "name":            g.name,
            "is_auto_matched": g.is_auto_matched,
            "created_at":      str(g.created_at),
            "member_count":    len(g.members),
            "members": [
                {"id": m.student.id, "name": m.student.name}
                for m in g.members
            ],
            "i_am_member": g.id in my_group_ids,
        }
        for g in groups
    ]


@router.post("/course/{course_id}")
def create_group(
    course_id: int,
    data: GroupCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    g = models.StudyGroup(course_id=course_id, name=data.name)
    db.add(g)
    db.flush()
    # Creator auto-joins if student
    if current_user.role == "student":
        db.add(models.StudyGroupMember(group_id=g.id, student_id=current_user.id))
    db.commit()
    db.refresh(g)
    return {"id": g.id, "name": g.name}


@router.post("/{group_id}/join")
def join_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    g = db.query(models.StudyGroup).filter(models.StudyGroup.id == group_id).first()
    if not g:
        raise HTTPException(404, "Group not found")
    if any(m.student_id == current_user.id for m in g.members):
        raise HTTPException(400, "Already in this group")
    db.add(models.StudyGroupMember(group_id=group_id, student_id=current_user.id))
    db.commit()
    return {"ok": True}


@router.delete("/{group_id}/leave")
def leave_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    member = db.query(models.StudyGroupMember).filter(
        models.StudyGroupMember.group_id   == group_id,
        models.StudyGroupMember.student_id == current_user.id,
    ).first()
    if not member:
        raise HTTPException(404, "You are not in this group")
    db.delete(member)
    db.commit()
    return {"ok": True}


@router.delete("/{group_id}")
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    g = db.query(models.StudyGroup).filter(models.StudyGroup.id == group_id).first()
    if not g:
        raise HTTPException(404, "Group not found")
    # Verify the caller owns the group's course
    security.require_course_access(g.course_id, current_user, db)
    db.delete(g)
    db.commit()
    return {"ok": True}


@router.post("/course/{course_id}/auto-match")
def auto_match(
    course_id: int,
    group_size: int = 3,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """
    Delete existing auto-matched groups for this course and regenerate them
    based on complementary quiz/assignment performance.
    """
    if group_size < 2 or group_size > 20:
        raise HTTPException(400, "group_size must be between 2 and 20")
    security.require_course_access(course_id, current_user, db)

    # Remove previous auto-matched groups
    old = (
        db.query(models.StudyGroup)
        .filter(
            models.StudyGroup.course_id       == course_id,
            models.StudyGroup.is_auto_matched == True,
        )
        .all()
    )
    for g in old:
        db.delete(g)
    db.flush()

    groups = _auto_match(course_id, group_size, db)
    created = []
    for i, member_ids in enumerate(groups, 1):
        g = models.StudyGroup(
            course_id=course_id,
            name=f"Study Group {i}",
            is_auto_matched=True,
        )
        db.add(g)
        db.flush()
        for sid in member_ids:
            db.add(models.StudyGroupMember(group_id=g.id, student_id=sid))
        created.append({"group": f"Study Group {i}", "members": len(member_ids)})

    db.commit()
    return {"groups_created": len(created), "groups": created}
