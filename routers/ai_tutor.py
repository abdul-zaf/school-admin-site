"""
ai_tutor.py — AI tutoring powered by a local Ollama model.

Knowledge base
--------------
Each student's knowledge base is built from the materials of every course
they are enrolled in.  Chunks are re-indexed automatically whenever a
material is added or deleted.  Only enrolled-course content is visible —
so two students with different enrolments see different knowledge.

Quiz / test restriction
-----------------------
If the student has any unsubmitted quiz attempt (active quiz in progress)
the AI tutor is locked: POST …/messages returns 403.

Assignment-help mode
--------------------
Sessions created with mode="assignment_help" (or linked to an assignment_id)
force the AI to give HINTS ONLY — it will never write the answer for the
student.  If the student asks for the direct answer the AI reminds them it
can only guide, not solve.

Environment variables
---------------------
OLLAMA_BASE_URL  (default: http://127.0.0.1:11434)
OLLAMA_MODEL     (default: llama3.2)
OLLAMA_TIMEOUT   (default: 60)

Endpoints
---------
GET    /api/ai-tutor/status
POST   /api/ai-tutor/sessions
GET    /api/ai-tutor/sessions
GET    /api/ai-tutor/sessions/{id}
DELETE /api/ai-tutor/sessions/{id}
POST   /api/ai-tutor/sessions/{id}/messages
GET    /api/ai-tutor/sessions/{id}/messages
GET    /api/ai-tutor/knowledge                         Student's own KB summary
GET    /api/ai-tutor/knowledge/{course_id}             Course KB detail (teacher/admin)
POST   /api/ai-tutor/knowledge/rebuild/{course_id}     Force-rebuild KB (teacher/admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from typing import Optional
from database import get_db
import models
import security
from services.ollama import (
    chat as ollama_chat,
    is_available as ollama_available,
    OLLAMA_MODEL,
)
from services.knowledge_base import (
    get_relevant_chunks,
    rebuild_course_knowledge,
    get_knowledge_summary,
)

router = APIRouter()

_VALID_MODES = {"study", "assignment_help"}


# ── Schemas ───────────────────────────────────────────────────────────────────

class SessionCreate(BaseModel):
    course_id:     Optional[int] = None
    assignment_id: Optional[int] = None
    title:         Optional[str] = None
    mode:          str = "study"

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        if v not in _VALID_MODES:
            raise ValueError(f"mode must be one of: {', '.join(_VALID_MODES)}")
        return v


class MessageCreate(BaseModel):
    content: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _active_quiz_attempt(db: Session, student_id: int) -> Optional[models.QuizAttempt]:
    """Return the active (unsubmitted) quiz attempt for this student, if any."""
    return (
        db.query(models.QuizAttempt)
        .filter(
            models.QuizAttempt.student_id == student_id,
            models.QuizAttempt.submitted_at == None,   # noqa: E711
        )
        .first()
    )


def _build_system_prompt(
    db: Session,
    session: models.TutorSession,
    student: models.User,
    query: str,
) -> str:
    """Build the full system prompt for this student's message."""
    lines = [
        "You are an AI tutor embedded in a school Learning Management System.",
        f"You are helping student: {student.name}.",
    ]

    # ── Course context ───────────────────────────────────────────────────────
    if session.course:
        lines.append(f"The student is currently studying: {session.course.title}.")

    # ── Assignment-help mode ─────────────────────────────────────────────────
    if session.mode == "assignment_help":
        lines.append(
            "\nMODE: ASSIGNMENT HELP (hints only)\n"
            "CRITICAL RULES you must ALWAYS follow in this mode:\n"
            "1. NEVER write the complete answer, solution, or finished work for the student.\n"
            "2. Give HINTS, guiding questions, and conceptual explanations instead.\n"
            "3. If the student asks you to 'just tell me the answer' or 'do this for me', "
            "   politely refuse and instead offer a targeted hint.\n"
            "4. Your goal is to help the student UNDERSTAND and arrive at the answer themselves.\n"
            "5. You may confirm whether the student's reasoning is on the right track.\n"
        )
        if session.assignment:
            a = session.assignment
            lines.append(
                f"The student is seeking help with assignment: \"{a.title}\"."
            )
            if a.description:
                lines.append(f"Assignment context: {a.description[:400]}")
    else:
        # Study mode — still never hand out quiz/test answers
        lines.append(
            "\nYou are in STUDY mode: help the student learn and understand concepts. "
            "Be thorough and educational. "
            "Do not solve graded assignments or quizzes for the student."
        )

    # ── Knowledge base context ───────────────────────────────────────────────
    chunks = get_relevant_chunks(
        db,
        student.id,
        query,
        course_id=session.course_id,
    )
    if chunks:
        lines.append(
            "\n--- KNOWLEDGE BASE (from enrolled course materials) ---\n"
            + "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(chunks))
            + "\n--- END KNOWLEDGE BASE ---"
        )
        lines.append(
            "Base your answers on the knowledge base above. "
            "If a topic is not covered there, say so and explain what you do know."
        )
    else:
        lines.append(
            "No specific course materials are indexed yet for this query. "
            "Answer from general knowledge but encourage the student to check course materials."
        )

    lines.append("Be concise, clear, and encouraging.")
    return "\n".join(lines)


# ── Status ────────────────────────────────────────────────────────────────────

@router.get("/status")
def tutor_status(
    current_user: models.User = Depends(security.get_current_user),
):
    available = ollama_available()
    return {
        "available": available,
        "model": OLLAMA_MODEL,
        "message": "Ollama is running" if available
                   else f"Ollama is not reachable. Run: ollama serve && ollama pull {OLLAMA_MODEL}",
    }


# ── Sessions ──────────────────────────────────────────────────────────────────

@router.post("/sessions")
def create_session(
    data: SessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    # Validate assignment belongs to an enrolled course
    if data.assignment_id:
        assignment = db.query(models.Assignment).filter(
            models.Assignment.id == data.assignment_id
        ).first()
        if not assignment:
            raise HTTPException(404, "Assignment not found")
        enrolled = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == assignment.course_id,
            models.Enrollment.student_id == current_user.id,
        ).first()
        if not enrolled:
            raise HTTPException(403, "You are not enrolled in the course for this assignment")
        # Auto-set course_id and mode when assignment provided
        if not data.course_id:
            data.course_id = assignment.course_id
        if data.mode == "study":
            data.mode = "assignment_help"

    # Validate course enrolment
    if data.course_id:
        enrolled = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == data.course_id,
            models.Enrollment.student_id == current_user.id,
        ).first()
        if not enrolled:
            raise HTTPException(403, "You are not enrolled in this course")

    title = data.title or (
        f"Assignment Help: {db.query(models.Assignment).filter(models.Assignment.id == data.assignment_id).first().title}"
        if data.assignment_id else "New Study Session"
    )
    session = models.TutorSession(
        student_id=current_user.id,
        course_id=data.course_id,
        assignment_id=data.assignment_id,
        title=title,
        mode=data.mode,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {
        "id": session.id,
        "title": session.title,
        "mode": session.mode,
        "course_id": session.course_id,
        "assignment_id": session.assignment_id,
        "created_at": str(session.created_at),
    }


@router.get("/sessions")
def list_sessions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    sessions = (
        db.query(models.TutorSession)
        .filter(models.TutorSession.student_id == current_user.id)
        .order_by(models.TutorSession.created_at.desc())
        .all()
    )
    return [
        {
            "id": s.id,
            "title": s.title,
            "mode": s.mode,
            "course_id": s.course_id,
            "course_title": s.course.title if s.course else None,
            "assignment_id": s.assignment_id,
            "assignment_title": s.assignment.title if s.assignment else None,
            "message_count": len(s.messages),
            "created_at": str(s.created_at),
        }
        for s in sessions
    ]


@router.get("/sessions/{session_id}")
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    session = db.query(models.TutorSession).filter(
        models.TutorSession.id == session_id,
        models.TutorSession.student_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")
    return {
        "id": session.id,
        "title": session.title,
        "mode": session.mode,
        "course_id": session.course_id,
        "course_title": session.course.title if session.course else None,
        "assignment_id": session.assignment_id,
        "assignment_title": session.assignment.title if session.assignment else None,
        "message_count": len(session.messages),
        "created_at": str(session.created_at),
    }


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    session = db.query(models.TutorSession).filter(
        models.TutorSession.id == session_id,
        models.TutorSession.student_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")
    db.delete(session)
    db.commit()
    return {"ok": True}


# ── Messages ──────────────────────────────────────────────────────────────────

@router.post("/sessions/{session_id}/messages")
def send_message(
    session_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    # ── 1. Quiz/test lock ────────────────────────────────────────────────────
    active = _active_quiz_attempt(db, current_user.id)
    if active:
        quiz = db.query(models.Quiz).filter(models.Quiz.id == active.quiz_id).first()
        quiz_title = quiz.title if quiz else "a quiz"
        raise HTTPException(
            403,
            f"The AI tutor is locked while you have an active quiz in progress "
            f"(\"{quiz_title}\"). Submit your quiz first.",
        )

    # ── 2. Ollama availability ───────────────────────────────────────────────
    if not ollama_available():
        raise HTTPException(
            503,
            f"AI tutor is not available. Make sure Ollama is running: "
            f"ollama serve && ollama pull {OLLAMA_MODEL}",
        )

    # ── 3. Load session ──────────────────────────────────────────────────────
    session = db.query(models.TutorSession).filter(
        models.TutorSession.id == session_id,
        models.TutorSession.student_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")

    # ── 4. Build system prompt with KB context ───────────────────────────────
    system_prompt = _build_system_prompt(db, session, current_user, data.content)

    # ── 5. Conversation history ──────────────────────────────────────────────
    history = (
        db.query(models.TutorMessage)
        .filter(models.TutorMessage.session_id == session_id)
        .order_by(models.TutorMessage.created_at)
        .all()
    )
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": data.content})

    # ── 6. Persist user message ──────────────────────────────────────────────
    user_msg = models.TutorMessage(
        session_id=session_id, role="user", content=data.content
    )
    db.add(user_msg)
    db.flush()

    # ── 7. Call Ollama ───────────────────────────────────────────────────────
    try:
        reply = ollama_chat(messages, system=system_prompt)
    except RuntimeError as exc:
        db.rollback()
        raise HTTPException(502, f"AI service error: {exc}")

    # ── 8. Persist assistant reply ───────────────────────────────────────────
    asst_msg = models.TutorMessage(
        session_id=session_id, role="assistant", content=reply
    )
    db.add(asst_msg)
    db.commit()

    return {
        "id": asst_msg.id,
        "role": "assistant",
        "content": reply,
        "mode": session.mode,
        "created_at": str(asst_msg.created_at),
    }


@router.get("/sessions/{session_id}/messages")
def get_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    session = db.query(models.TutorSession).filter(
        models.TutorSession.id == session_id,
        models.TutorSession.student_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")
    msgs = (
        db.query(models.TutorMessage)
        .filter(models.TutorMessage.session_id == session_id)
        .order_by(models.TutorMessage.created_at)
        .all()
    )
    return [
        {"id": m.id, "role": m.role, "content": m.content, "created_at": str(m.created_at)}
        for m in msgs
    ]


# ── Knowledge base endpoints ──────────────────────────────────────────────────

@router.get("/knowledge")
def my_knowledge_base(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    """Return a summary of the knowledge the AI has about each enrolled course."""
    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == current_user.id
    ).all()
    result = []
    for enr in enrollments:
        course = enr.course
        summary = get_knowledge_summary(db, course.id)
        result.append({
            "course_id": course.id,
            "course_title": course.title,
            **summary,
            "is_indexed": summary["total_chunks"] > 0,
        })
    return result


@router.get("/knowledge/{course_id}")
def course_knowledge_detail(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """List all knowledge chunks indexed for a course (teacher/admin)."""
    security.require_course_access(course_id, current_user, db)
    chunks = (
        db.query(models.KnowledgeChunk)
        .filter(models.KnowledgeChunk.course_id == course_id)
        .order_by(models.KnowledgeChunk.chunk_type, models.KnowledgeChunk.id)
        .all()
    )
    summary = get_knowledge_summary(db, course_id)
    return {
        "course_id": course_id,
        **summary,
        "chunks": [
            {
                "id": c.id,
                "chunk_type": c.chunk_type,
                "material_id": c.material_id,
                "preview": c.chunk_text[:120] + ("…" if len(c.chunk_text) > 120 else ""),
                "keyword_count": len(c.keywords.split()) if c.keywords else 0,
            }
            for c in chunks
        ],
    }


@router.post("/knowledge/rebuild/{course_id}")
def rebuild_knowledge(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin", "teacher")),
):
    """Force-rebuild the knowledge base for a course (teacher/admin)."""
    security.require_course_access(course_id, current_user, db)
    count = rebuild_course_knowledge(db, course_id)
    return {"ok": True, "course_id": course_id, "chunks_created": count}
