"""
code_sandbox.py — Safe Python code execution sandbox.

POST /api/sandbox/run      Execute Python code (student)
GET  /api/sandbox/history  Own code submission history (student)
"""
import subprocess
import sys
import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import security

router = APIRouter()

ALLOWED_LANGUAGES = {"python"}
TIMEOUT_SECONDS = 10
MAX_OUTPUT_CHARS = 10000

# Dangerous imports that are blocked
DANGEROUS_IMPORTS = [
    "import os",
    "import sys",
    "import subprocess",
    "import socket",
    "from os",
    "from sys",
    "from subprocess",
    "from socket",
    "__import__",
    "open(",
    "exec(",
    "eval(",
    "compile(",
]


def _check_dangerous(code: str) -> Optional[str]:
    """Return a message if dangerous code patterns are found."""
    lower = code.lower()
    for pattern in DANGEROUS_IMPORTS:
        if pattern in lower:
            return f"Dangerous code pattern detected: '{pattern}' is not allowed"
    return None


class RunRequest(BaseModel):
    language: str
    code: str
    stdin: Optional[str] = None
    assignment_id: Optional[int] = None


@router.post("/run")
def run_code(
    data: RunRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    if data.language not in ALLOWED_LANGUAGES:
        raise HTTPException(400, f"Only {ALLOWED_LANGUAGES} are supported")

    danger = _check_dangerous(data.code)
    if danger:
        raise HTTPException(400, danger)

    start_ms = time.time() * 1000
    try:
        result = subprocess.run(
            [sys.executable, "-c", data.code],
            input=data.stdin or "",
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        stdout = result.stdout[:MAX_OUTPUT_CHARS]
        stderr = result.stderr[:MAX_OUTPUT_CHARS]
        exit_code = result.returncode
    except subprocess.TimeoutExpired:
        stdout = ""
        stderr = f"Execution timed out after {TIMEOUT_SECONDS} seconds"
        exit_code = -1
    except Exception as e:
        stdout = ""
        stderr = str(e)
        exit_code = -1

    elapsed_ms = int(time.time() * 1000 - start_ms)

    # Store submission
    sub = models.CodeSubmission(
        assignment_id=data.assignment_id,
        student_id=current_user.id,
        language=data.language,
        code=data.code,
        stdin=data.stdin,
        stdout=stdout,
        stderr=stderr,
        exit_code=exit_code,
        execution_time_ms=elapsed_ms,
    )
    db.add(sub)
    db.commit()

    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "execution_time_ms": elapsed_ms,
        "submission_id": sub.id,
    }


@router.get("/history")
def code_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    subs = (
        db.query(models.CodeSubmission)
        .filter(models.CodeSubmission.student_id == current_user.id)
        .order_by(models.CodeSubmission.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": s.id,
            "language": s.language,
            "code": s.code[:200] + ("..." if len(s.code) > 200 else ""),
            "exit_code": s.exit_code,
            "execution_time_ms": s.execution_time_ms,
            "assignment_id": s.assignment_id,
            "created_at": str(s.created_at),
        }
        for s in subs
    ]
