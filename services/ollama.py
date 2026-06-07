"""
services/ollama.py — Thin wrapper around the Ollama REST API.

Ollama exposes a local HTTP server (default http://localhost:11434).
No external package required — uses Python's stdlib urllib.

Environment variables:
  OLLAMA_BASE_URL   Base URL of Ollama server  (default: http://localhost:11434)
  OLLAMA_MODEL      Model name to use          (default: llama3.2)
  OLLAMA_TIMEOUT    Request timeout in seconds (default: 60)
"""
import json
import os
import urllib.error
import urllib.request
from typing import Optional, List

OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL: str    = os.getenv("OLLAMA_MODEL",    "llama3.2")
OLLAMA_TIMEOUT: int  = int(os.getenv("OLLAMA_TIMEOUT", "600"))


# ── Public helpers ────────────────────────────────────────────────────────────

def is_available() -> bool:
    """Return True if the Ollama server responds to a health-check ping."""
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE_URL}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5):
            return True
    except Exception:
        return False


def chat(
    messages: list[dict],
    *,
    system: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    num_ctx: Optional[int] = None,
    images: Optional[List[str]] = None,
) -> str:
    """
    Send a chat request to Ollama and return the assistant's text reply.

    Parameters
    ----------
    messages   : list of {"role": "user"|"assistant", "content": str}
    system     : optional system-prompt prepended as a {"role": "system"} message
    model      : override OLLAMA_MODEL for this call
    temperature: sampling temperature (0.0 = deterministic)
    max_tokens : maximum tokens in the reply (passed as num_predict option)
    images     : optional list of base64-encoded image strings attached to the
                 latest user message. Requires a vision-capable model such as
                 llava or llama3.2-vision (set OLLAMA_MODEL accordingly).

    Returns
    -------
    str  — the assistant reply text

    Raises
    ------
    RuntimeError  on network error or non-200 response
    """
    m = list(messages)
    if system:
        m = [{"role": "system", "content": system}] + m

    # Attach images to the last user message when provided
    if images:
        for i in range(len(m) - 1, -1, -1):
            if m[i]["role"] == "user":
                m[i] = {**m[i], "images": images}
                break

    options: dict = {"temperature": temperature, "num_predict": max_tokens}
    if num_ctx is not None:
        options["num_ctx"] = num_ctx

    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": m,
        "stream": False,
        "options": options,
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{OLLAMA_BASE_URL}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
            return data["message"]["content"]
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Ollama HTTP {exc.code}: {exc.read().decode(errors='replace')}") from exc
    except Exception as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc


def generate(prompt: str, *, model: Optional[str] = None, max_tokens: int = 512) -> str:
    """
    Simple single-turn generate (no conversation history).
    Useful for short grading / classification tasks.
    """
    return chat(
        [{"role": "user", "content": prompt}],
        model=model,
        temperature=0.0,      # deterministic for grading
        max_tokens=max_tokens,
    )
