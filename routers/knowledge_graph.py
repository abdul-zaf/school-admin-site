"""
Cross-course knowledge graph.

Admins and teachers create Concepts (nodes) and ConceptLinks (edges).
Courses are tagged to concepts so students can see how their subjects connect.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
import models
import security

router = APIRouter()


class ConceptCreate(BaseModel):
    name: str
    description: Optional[str] = None
    color: str = "#2563eb"


class LinkCreate(BaseModel):
    from_id: int
    to_id: int
    label: str = "relates to"


class TagCreate(BaseModel):
    course_id: int


# ── Read ──────────────────────────────────────────────────────────────────────

@router.get("/")
def get_graph(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    """Return the full graph: all concepts (nodes) and links (edges)."""
    concepts = db.query(models.Concept).all()
    links    = db.query(models.ConceptLink).all()

    nodes = [
        {
            "id":          c.id,
            "name":        c.name,
            "description": c.description,
            "color":       c.color,
            "courses": [
                {"id": t.course.id, "title": t.course.title}
                for t in c.course_tags
            ],
        }
        for c in concepts
    ]
    edges = [
        {
            "id":    lk.id,
            "from":  lk.from_id,
            "to":    lk.to_id,
            "label": lk.label,
        }
        for lk in links
    ]
    return {"nodes": nodes, "edges": edges}


# ── Concepts ──────────────────────────────────────────────────────────────────

@router.post("/concepts")
def create_concept(
    data: ConceptCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    if db.query(models.Concept).filter(models.Concept.name == data.name.strip()).first():
        raise HTTPException(400, "A concept with that name already exists")
    c = models.Concept(name=data.name.strip(), description=data.description, color=data.color)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "name": c.name}


@router.put("/concepts/{concept_id}")
def update_concept(
    concept_id: int,
    data: ConceptCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    c = db.query(models.Concept).filter(models.Concept.id == concept_id).first()
    if not c:
        raise HTTPException(404, "Concept not found")
    c.name        = data.name.strip()
    c.description = data.description
    c.color       = data.color
    db.commit()
    return {"ok": True}


@router.delete("/concepts/{concept_id}")
def delete_concept(
    concept_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    c = db.query(models.Concept).filter(models.Concept.id == concept_id).first()
    if not c:
        raise HTTPException(404, "Concept not found")
    db.delete(c)
    db.commit()
    return {"ok": True}


# ── Links ─────────────────────────────────────────────────────────────────────

@router.post("/links")
def create_link(
    data: LinkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    if data.from_id == data.to_id:
        raise HTTPException(400, "A concept cannot link to itself")
    lk = models.ConceptLink(from_id=data.from_id, to_id=data.to_id, label=data.label)
    db.add(lk)
    db.commit()
    db.refresh(lk)
    return {"id": lk.id}


@router.delete("/links/{link_id}")
def delete_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    lk = db.query(models.ConceptLink).filter(models.ConceptLink.id == link_id).first()
    if not lk:
        raise HTTPException(404, "Link not found")
    db.delete(lk)
    db.commit()
    return {"ok": True}


# ── Course tags ───────────────────────────────────────────────────────────────

@router.post("/concepts/{concept_id}/tag")
def tag_course(
    concept_id: int,
    data: TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    existing = db.query(models.ConceptCourseTag).filter(
        models.ConceptCourseTag.concept_id == concept_id,
        models.ConceptCourseTag.course_id  == data.course_id,
    ).first()
    if existing:
        raise HTTPException(400, "Course already tagged to this concept")
    t = models.ConceptCourseTag(concept_id=concept_id, course_id=data.course_id)
    db.add(t)
    db.commit()
    return {"ok": True}


@router.delete("/concepts/{concept_id}/tag/{course_id}")
def untag_course(
    concept_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    t = db.query(models.ConceptCourseTag).filter(
        models.ConceptCourseTag.concept_id == concept_id,
        models.ConceptCourseTag.course_id  == course_id,
    ).first()
    if not t:
        raise HTTPException(404, "Tag not found")
    db.delete(t)
    db.commit()
    return {"ok": True}
