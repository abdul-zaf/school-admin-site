"""
services/file_extractor.py — Extract text from uploaded files for AI tutor context.

Supported types
---------------
Text / code   .txt .py .js .ts .jsx .tsx .java .c .cpp .h .cs .go .rb .php
              .swift .html .htm .css .md .csv .json .xml .yaml .yml .sh .sql
              .r .rs .kt .scala → read as UTF-8, truncated to MAX_TEXT_CHARS

PDF           .pdf → text extracted page by page via pypdf (soft dependency;
              falls back to filename-only if pypdf is not installed)

Word          .docx → text extracted via python-docx (soft dependency;
              falls back to filename-only if not installed)

Images        .jpg .jpeg .png .gif .webp .bmp → returned as raw bytes;
              caller base64-encodes and sends to a vision-capable Ollama model

Unsupported   anything else → returns None (file is skipped in AI context)

Constants
---------
MAX_TEXT_CHARS  Maximum characters extracted per file injected into prompt.
                Large files are truncated with a notice.
MAX_PDF_PAGES   Maximum pages extracted from a PDF.
"""

import base64
import os
from pathlib import Path
from typing import Optional, Tuple

# ── Limits ────────────────────────────────────────────────────────────────────
MAX_TEXT_CHARS = 3000    # chars injected per text file
MAX_PDF_PAGES  = 15      # pages read from a PDF

# ── File classification ───────────────────────────────────────────────────────
_TEXT_EXTS = {
    ".txt", ".py", ".js", ".mjs", ".cjs", ".ts", ".jsx", ".tsx",
    ".java", ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".cs",
    ".go", ".rb", ".php", ".swift", ".kt", ".scala", ".m",
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".md", ".markdown", ".rst",
    ".csv", ".tsv", ".json", ".jsonl", ".xml", ".yaml", ".yml", ".toml", ".ini",
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
    ".sql", ".r", ".rs", ".lua", ".pl", ".pm", ".ex", ".exs",
    ".vue", ".svelte",
}
_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"}
_PDF_EXTS   = {".pdf"}
_DOCX_EXTS  = {".docx"}


def classify(filename: str, mime: str = "") -> str:
    """Return 'text' | 'pdf' | 'docx' | 'image' | 'unsupported'."""
    ext = Path(filename).suffix.lower()
    if ext in _TEXT_EXTS or mime.startswith("text/"):
        return "text"
    if ext in _PDF_EXTS or mime == "application/pdf":
        return "pdf"
    if ext in _DOCX_EXTS or "wordprocessingml" in mime:
        return "docx"
    if ext in _IMAGE_EXTS or mime.startswith("image/"):
        return "image"
    return "unsupported"


# ── Extraction functions ──────────────────────────────────────────────────────

def _read_text_file(path: str) -> str:
    """Read a plain-text file, trying UTF-8 then latin-1."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def _extract_pdf(path: str) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(path)
        pages = reader.pages[:MAX_PDF_PAGES]
        parts = []
        for i, page in enumerate(pages, 1):
            try:
                text = page.extract_text() or ""
                if text.strip():
                    parts.append(f"[Page {i}]\n{text.strip()}")
            except Exception:
                pass
        total = len(reader.pages)
        result = "\n\n".join(parts)
        if total > MAX_PDF_PAGES:
            result += f"\n\n[…truncated: showing {MAX_PDF_PAGES}/{total} pages]"
        return result
    except ImportError:
        return "[PDF text extraction requires pypdf — pip install pypdf]"
    except Exception as exc:
        return f"[PDF extraction failed: {exc}]"


def _extract_docx(path: str) -> str:
    try:
        import docx
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        return "[DOCX extraction requires python-docx — pip install python-docx]"
    except Exception as exc:
        return f"[DOCX extraction failed: {exc}]"


def _load_image_b64(path: str) -> Optional[str]:
    """Read an image file and return its base64 encoding (no header)."""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


# ── Public API ────────────────────────────────────────────────────────────────

def extract(
    path: str,
    filename: str,
    mime: str = "",
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract content from an uploaded file.

    Returns
    -------
    (text, image_b64)
      text      : extracted text string, truncated to MAX_TEXT_CHARS, or None
      image_b64 : raw base64 image string (no data-URI prefix) for vision
                  models, or None

    For unsupported file types both values are None.
    """
    kind = classify(filename, mime)

    if kind == "text":
        raw = _read_text_file(path)
        if len(raw) > MAX_TEXT_CHARS:
            raw = raw[:MAX_TEXT_CHARS] + f"\n\n[…truncated at {MAX_TEXT_CHARS} characters]"
        return raw or None, None

    if kind == "pdf":
        raw = _extract_pdf(path)
        if len(raw) > MAX_TEXT_CHARS:
            raw = raw[:MAX_TEXT_CHARS] + f"\n\n[…truncated at {MAX_TEXT_CHARS} characters]"
        return raw or None, None

    if kind == "docx":
        raw = _extract_docx(path)
        if len(raw) > MAX_TEXT_CHARS:
            raw = raw[:MAX_TEXT_CHARS] + f"\n\n[…truncated at {MAX_TEXT_CHARS} characters]"
        return raw or None, None

    if kind == "image":
        return None, _load_image_b64(path)

    return None, None   # unsupported


def format_for_prompt(filename: str, text: str) -> str:
    """Wrap extracted text in a clearly labelled block for the AI prompt."""
    ext = Path(filename).suffix.lstrip(".").lower() or "text"
    return (
        f"[Attached file: {filename}]\n"
        f"```{ext}\n"
        f"{text}\n"
        f"```\n"
        f"[End of {filename}]"
    )
