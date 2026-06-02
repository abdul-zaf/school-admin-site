"""
services/knowledge_base.py — Per-course knowledge base for the AI tutor.

Text is extracted from every course material and assignment description,
broken into searchable chunks, and stored in knowledge_chunks.  When the
AI tutor handles a student message it calls get_relevant_chunks() which
uses a lightweight TF-IDF-style keyword score to pick the most useful
context to inject into Ollama's system prompt.

Auto-update hooks
-----------------
index_material(db, material)       — call after any material create/update
remove_material_index(db, mat_id)  — call after material delete
rebuild_course_knowledge(db, cid)  — full rebuild (teacher-triggered or on-demand)
"""
import re
from typing import List
from sqlalchemy.orm import Session

import models

# ── Tuning constants ──────────────────────────────────────────────────────────
MAX_CHUNK_CHARS    = 800   # characters per stored chunk
MAX_INJECT_CHUNKS  = 6     # max chunks injected into a single AI prompt
MIN_MATCH_WORDS    = 1     # minimum keyword overlap to include a chunk

# Stop words to exclude from keyword index (English only, keep it tiny)
_STOP = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "be", "been", "has", "have",
    "had", "do", "does", "did", "will", "would", "can", "could", "should",
    "may", "might", "this", "that", "these", "those", "it", "its", "by",
    "from", "up", "as", "into", "not", "no", "if", "so", "than",
})


# ── Internal helpers ──────────────────────────────────────────────────────────

def _words(text: str) -> List[str]:
    """Return lowercase words ≥ 3 chars, excluding stop-words."""
    return [
        w for w in re.findall(r"\b[a-z]{3,}\b", text.lower())
        if w not in _STOP
    ]


def _split(text: str) -> List[str]:
    """Split text into MAX_CHUNK_CHARS chunks on sentence / word boundaries."""
    text = text.strip()
    if len(text) <= MAX_CHUNK_CHARS:
        return [text] if text else []
    chunks = []
    while text:
        if len(text) <= MAX_CHUNK_CHARS:
            chunks.append(text)
            break
        # Try to cut at last sentence boundary before the limit
        cut = text[:MAX_CHUNK_CHARS].rfind(". ")
        if cut < MAX_CHUNK_CHARS // 2:
            # No good sentence boundary; cut at last space
            cut = text[:MAX_CHUNK_CHARS].rfind(" ")
        if cut <= 0:
            cut = MAX_CHUNK_CHARS
        chunks.append(text[:cut].strip())
        text = text[cut:].strip()
    return [c for c in chunks if c]


def _material_text(m: "models.Material") -> str:
    """Assemble the searchable text for one material."""
    parts = [f"Material: {m.title}"]
    if m.content:
        parts.append(m.content)
    if m.url:
        parts.append(f"Reference: {m.url}")
    # For file materials include the filename as a clue
    if m.file_name:
        parts.append(f"File: {m.file_name}")
    return "\n".join(parts)


def _build_chunk(course_id: int, material_id, chunk_type: str, text: str) -> "models.KnowledgeChunk":
    kws = " ".join(sorted(set(_words(text))))
    return models.KnowledgeChunk(
        course_id=course_id,
        material_id=material_id,
        chunk_type=chunk_type,
        chunk_text=text,
        keywords=kws,
    )


# ── Public API ────────────────────────────────────────────────────────────────

def index_material(db: Session, material: "models.Material") -> None:
    """
    Create (or replace) KnowledgeChunks for one material.
    Call this every time a material is created or its content changes.
    Caller must db.commit() afterwards.
    """
    # Remove old chunks for this exact material
    db.query(models.KnowledgeChunk).filter(
        models.KnowledgeChunk.material_id == material.id
    ).delete(synchronize_session=False)

    text = _material_text(material)
    for chunk in _split(text):
        db.add(_build_chunk(material.course_id, material.id, "material", chunk))


def remove_material_index(db: Session, material_id: int) -> None:
    """
    Delete all KnowledgeChunks for a material that is being removed.
    Caller must db.commit() afterwards.
    """
    db.query(models.KnowledgeChunk).filter(
        models.KnowledgeChunk.material_id == material_id
    ).delete(synchronize_session=False)


def index_assignment(db: Session, assignment: "models.Assignment") -> None:
    """
    Index an assignment's description so the tutor knows what it's about
    without revealing the answer.  Call after create/update.
    Caller must db.commit() afterwards.
    """
    # Remove old assignment chunks for this assignment (no material_id)
    # We tag them by looking for chunks with a matching prefix in chunk_text —
    # safer: store assignment_id in a separate column.  Here we delete by
    # course + type + text prefix match.  Simple approach: delete all
    # "assignment" type chunks for this course and re-index all assignments.
    _rebuild_assignment_chunks(db, assignment.course_id)


def _rebuild_assignment_chunks(db: Session, course_id: int) -> None:
    """Re-index all assignment descriptions for one course (cheap, fast)."""
    db.query(models.KnowledgeChunk).filter(
        models.KnowledgeChunk.course_id == course_id,
        models.KnowledgeChunk.chunk_type == "assignment",
    ).delete(synchronize_session=False)

    assignments = db.query(models.Assignment).filter(
        models.Assignment.course_id == course_id
    ).all()
    for a in assignments:
        if not a.description and not a.title:
            continue
        text = f"Assignment — {a.title}"
        if a.description:
            text += f"\nContext: {a.description[:600]}"
        for chunk in _split(text):
            db.add(_build_chunk(course_id, None, "assignment", chunk))


def rebuild_course_knowledge(db: Session, course_id: int) -> int:
    """
    Full rebuild: drop all chunks for this course and re-index everything.
    Returns the number of chunks created.
    Used by the teacher-triggered endpoint and on first boot.
    """
    db.query(models.KnowledgeChunk).filter(
        models.KnowledgeChunk.course_id == course_id
    ).delete(synchronize_session=False)

    count = 0
    for material in db.query(models.Material).filter(
        models.Material.course_id == course_id
    ).all():
        text = _material_text(material)
        for chunk in _split(text):
            db.add(_build_chunk(course_id, material.id, "material", chunk))
            count += 1

    _rebuild_assignment_chunks(db, course_id)
    count += db.query(models.KnowledgeChunk).filter(
        models.KnowledgeChunk.course_id == course_id,
        models.KnowledgeChunk.chunk_type == "assignment",
    ).count()

    db.commit()
    return count


def get_relevant_chunks(
    db: Session,
    student_id: int,
    query: str,
    course_id: int | None = None,
) -> List[str]:
    """
    Return the most relevant knowledge chunks for this student's query.

    Only chunks from courses the student is enrolled in are considered —
    this is what makes the knowledge base *per-student*: two students
    enrolled in different courses see different knowledge.

    Parameters
    ----------
    db         : open SQLAlchemy session
    student_id : the asking student
    query      : the user's message text
    course_id  : if set, restrict search to this one course
    """
    # Determine which courses this student can access
    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id
    ).all()
    enrolled_ids = [e.course_id for e in enrollments]

    if not enrolled_ids:
        return []

    if course_id and course_id in enrolled_ids:
        search_ids = [course_id]
    elif course_id:
        return []          # student is not enrolled in the requested course
    else:
        search_ids = enrolled_ids

    # Load all chunks for accessible courses
    chunks = (
        db.query(models.KnowledgeChunk)
        .filter(models.KnowledgeChunk.course_id.in_(search_ids))
        .all()
    )
    if not chunks:
        return []

    # Score each chunk by keyword overlap with the query
    query_words = set(_words(query))
    if not query_words:
        # No meaningful query words — return top chunks by course order
        return [c.chunk_text for c in chunks[:MAX_INJECT_CHUNKS]]

    scored = []
    for chunk in chunks:
        chunk_words = set(chunk.keywords.split()) if chunk.keywords else set()
        overlap = len(query_words & chunk_words)
        if overlap >= MIN_MATCH_WORDS:
            scored.append((overlap, chunk.chunk_text))

    if not scored:
        # No keyword match — include a few generic chunks so the AI isn't empty
        return [c.chunk_text for c in chunks[:3]]

    scored.sort(key=lambda x: x[0], reverse=True)
    return [text for _, text in scored[:MAX_INJECT_CHUNKS]]


def get_knowledge_summary(db: Session, course_id: int) -> dict:
    """Return a summary of what's indexed for a course (for the status endpoint)."""
    total   = db.query(models.KnowledgeChunk).filter(
        models.KnowledgeChunk.course_id == course_id
    ).count()
    mat_cnt = db.query(models.KnowledgeChunk).filter(
        models.KnowledgeChunk.course_id == course_id,
        models.KnowledgeChunk.chunk_type == "material",
    ).count()
    asn_cnt = db.query(models.KnowledgeChunk).filter(
        models.KnowledgeChunk.course_id == course_id,
        models.KnowledgeChunk.chunk_type == "assignment",
    ).count()
    return {"total_chunks": total, "material_chunks": mat_cnt, "assignment_chunks": asn_cnt}
