"""
ai_tutor.py — AI tutoring sessions powered by a local Ollama model.

POST   /api/ai-tutor/sessions                Create tutoring session (student)
GET    /api/ai-tutor/sessions                List own sessions (student)
POST   /api/ai-tutor/sessions/{id}/messages  Send message and get AI response (student)
GET    /api/ai-tutor/sessions/{id}/messages  Message history (student)
DELETE /api/ai-tutor/sessions/{id}           Delete session (student)
GET    /api/ai-tutor/status                  Check whether Ollama is reachable (any auth)

Environment variables
---------------------
OLLAMA_BASE_URL  URL of Ollama server  (default: http://localhost:11434)
OLLAMA_MODEL     Model name to use     (default: llama3.2)
OLLAMA_TIMEOUT   Request timeout (s)   (default: 60)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import security
from services.ollama import chat as ollama_chat, is_available as ollama_available, OLLAMA_MODEL

router = APIRouter()


class SessionCreate(BaseModel):
    course_id: Optional[int] = None
    title: Optional[str] = None


class MessageCreate(BaseModel):
    content: str


# ── Status ────────────────────────────────────────────────────────────────────

@router.get("/status")
def tutor_status(
    current_user: models.User = Depends(security.get_current_user),
):
    """Return whether the Ollama backend is reachable and which model is in use."""
    available = ollama_available()
    return {
        "available": available,
        "model": OLLAMA_MODEL,
        "message": "Ollama is running" if available else
                   "Ollama is not reachable. Start it with: ollama serve",
    }


# ── Sessions ──────────────────────────────────────────────────────────────────

@router.post("/sessions")
def create_session(
    data: SessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    title = data.title or "New Session"
    session = models.TutorSession(
        student_id=current_user.id,
        course_id=data.course_id,
        title=title,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"id": session.id, "title": session.title, "created_at": str(session.created_at)}


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
            "course_id": s.course_id,
            "course_title": s.course.title if s.course else None,
            "message_count": len(s.messages),
            "created_at": str(s.created_at),
        }
        for s in sessions
    ]


@router.post("/sessions/{session_id}/messages")
def send_message(
    session_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    if not ollama_available():
        raise HTTPException(
            503,
            "AI tutor is not available. Make sure Ollama is running "
            f"(ollama serve) and the model '{OLLAMA_MODEL}' is pulled "
            f"(ollama pull {OLLAMA_MODEL}).",
        )

    session = db.query(models.TutorSession).filter(
        models.TutorSession.id == session_id,
        models.TutorSession.student_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")

    # Build system prompt with course context
    system_parts = [
        "You are a helpful AI tutor for a school Learning Management System.",
        f"You are helping student: {current_user.name}.",
    ]
    if session.course:
        system_parts.append(f"Course: {session.course.title}")
        materials = (
            db.query(models.Material)
            .filter(models.Material.course_id == session.course_id)
            .limit(10)
            .all()
        )
        if materials:
            titles = ", ".join(m.title for m in materials)
            system_parts.append(f"Course materials include: {titles}")
    system_parts.append(
        "Be concise, educational, and encouraging. "
        "Help the student understand concepts rather than just giving answers."
    )
    system_prompt = "\n".join(system_parts)

    # Load conversation history
    history = (
        db.query(models.TutorMessage)
        .filter(models.TutorMessage.session_id == session_id)
        .order_by(models.TutorMessage.created_at)
        .all()
    )
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": data.content})

    # Persist the user message
    user_msg = models.TutorMessage(
        session_id=session_id,
        role="user",
        content=data.content,
    )
    db.add(user_msg)
    db.flush()

    # Call Ollama
    try:
        assistant_content = ollama_chat(messages, system=system_prompt)
    except RuntimeError as exc:
        db.rollback()
        raise HTTPException(502, f"AI service error: {exc}")

    # Persist the assistant reply
    assistant_msg = models.TutorMessage(
        session_id=session_id,
        role="assistant",
        content=assistant_content,
    )
    db.add(assistant_msg)
    db.commit()

    return {
        "id": assistant_msg.id,
        "role": "assistant",
        "content": assistant_content,
        "created_at": str(assistant_msg.created_at),
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

    messages = (
        db.query(models.TutorMessage)
        .filter(models.TutorMessage.session_id == session_id)
        .order_by(models.TutorMessage.created_at)
        .all()
    )
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "created_at": str(m.created_at),
        }
        for m in messages
    ]


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
