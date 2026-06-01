"""
Password reset via email.

Flow:
  1. POST /api/auth/forgot-password   { email }
       → generates a secure token, saves to DB, sends email
       → always returns the same generic message (never reveals if email exists)

  2. GET  /api/auth/verify-reset-token/{token}
       → { "valid": true/false }  — used by the frontend to show/hide the form

  3. POST /api/auth/reset-password    { token, new_password }
       → validates token, hashes new password, marks token as used

Environment variables required for email:
  SMTP_HOST      default: smtp.gmail.com
  SMTP_PORT      default: 587
  SMTP_USER      your Gmail / SMTP address
  SMTP_PASSWORD  your Gmail App Password (not your Google account password)
  FROM_EMAIL     optional – defaults to SMTP_USER
  APP_URL        optional – auto-detected from RENDER_EXTERNAL_URL on Render

If SMTP_USER / SMTP_PASSWORD are not set the reset link is printed to the
server console instead — useful for local development without an email account.
"""
import os
import smtplib
import secrets
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
import models
import security

router = APIRouter()

_TOKEN_EXPIRE_HOURS = 1


# ── Helpers ───────────────────────────────────────────────────────────────────

def _app_url() -> str:
    return (
        os.getenv("APP_URL")
        or os.getenv("RENDER_EXTERNAL_URL", "")
        or "http://localhost:8000"
    ).rstrip("/")


def _send_reset_email(to_email: str, to_name: str, token: str) -> None:
    """Send the password-reset email.  Runs in a background thread."""
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASSWORD", "")
    from_email = os.getenv("FROM_EMAIL", smtp_user)

    reset_url = f"{_app_url()}/?reset={token}"

    if not smtp_user or not smtp_pass:
        # No SMTP configured – print to console for local dev
        print(
            f"\n{'='*60}\n"
            f"[PASSWORD RESET] Email not configured.\n"
            f"Reset link for {to_email}:\n{reset_url}\n"
            f"{'='*60}\n"
        )
        return

    html = f"""
    <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px">
      <div style="background:linear-gradient(135deg,#1e1b4b,#4f46e5);
                  padding:30px;border-radius:12px 12px 0 0;text-align:center">
        <h1 style="color:#fff;margin:0;font-size:28px">🎓 EduPortal</h1>
        <p style="color:rgba(255,255,255,.75);margin:6px 0 0;font-size:14px">
          School Learning Management System
        </p>
      </div>
      <div style="background:#fff;padding:32px;border:1px solid #e0e7ff;
                  border-top:none;border-radius:0 0 12px 12px">
        <h2 style="color:#1e1b4b;margin-top:0">Password Reset Request</h2>
        <p style="color:#374151">Hi <strong>{to_name}</strong>,</p>
        <p style="color:#374151">
          We received a request to reset your EduPortal password.
          Click the button below to choose a new one:
        </p>
        <div style="text-align:center;margin:32px 0">
          <a href="{reset_url}"
             style="background:#4f46e5;color:#fff;padding:14px 36px;
                    border-radius:8px;text-decoration:none;font-weight:700;
                    font-size:16px;display:inline-block">
            Reset My Password
          </a>
        </div>
        <p style="color:#6b7280;font-size:13px;line-height:1.6">
          ⏰ This link expires in <strong>1 hour</strong>.<br>
          🔒 If you did not request a password reset you can safely ignore this email —
          your password will not change.
        </p>
        <hr style="border:none;border-top:1px solid #e0e7ff;margin:24px 0">
        <p style="color:#9ca3af;font-size:12px;margin:0">
          Button not working? Paste this link into your browser:<br>
          <a href="{reset_url}" style="color:#4f46e5;word-break:break-all">{reset_url}</a>
        </p>
      </div>
    </body></html>
    """

    plain = (
        f"Hi {to_name},\n\n"
        f"Reset your EduPortal password here (valid for 1 hour):\n{reset_url}\n\n"
        f"If you did not request this, ignore this email.\n"
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "EduPortal — Password Reset"
    msg["From"]    = f"EduPortal <{from_email}>"
    msg["To"]      = to_email
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html,  "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"[PASSWORD RESET] Email sent to {to_email}")
    except Exception as exc:
        print(f"[PASSWORD RESET] Failed to send email to {to_email}: {exc}")


# ── Schemas ───────────────────────────────────────────────────────────────────

class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


# ── Endpoints ─────────────────────────────────────────────────────────────────

_GENERIC_RESPONSE = {
    "message": (
        "If that email address is registered you'll receive a reset link "
        "within a minute. Check your spam folder too."
    )
}


@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    # Rate-limit using the same limiter as login (10 req / 60 s per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not security.login_limiter.is_allowed(f"reset:{client_ip}"):
        raise HTTPException(429, "Too many requests. Please wait a minute and try again.")

    email = data.email.strip().lower()
    user  = db.query(models.User).filter(models.User.email == email).first()

    # Always return the generic message — never reveal whether the email exists
    if not user:
        return _GENERIC_RESPONSE

    # Invalidate any still-active tokens for this user to prevent link accumulation
    db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.user_id == user.id,
        models.PasswordResetToken.used    == False,           # noqa: E712
    ).update({"used": True})
    db.flush()

    token = secrets.token_urlsafe(32)
    db.add(models.PasswordResetToken(
        user_id    = user.id,
        token      = token,
        expires_at = datetime.utcnow() + timedelta(hours=_TOKEN_EXPIRE_HOURS),
    ))
    db.commit()

    background_tasks.add_task(_send_reset_email, user.email, user.name, token)
    return _GENERIC_RESPONSE


@router.get("/verify-reset-token/{token}")
def verify_reset_token(token: str, db: Session = Depends(get_db)):
    """Frontend calls this to check whether a reset link is still valid."""
    rt = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token      == token,
        models.PasswordResetToken.used       == False,        # noqa: E712
        models.PasswordResetToken.expires_at >  datetime.utcnow(),
    ).first()
    return {"valid": rt is not None}


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    rt = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token      == data.token,
        models.PasswordResetToken.used       == False,        # noqa: E712
        models.PasswordResetToken.expires_at >  datetime.utcnow(),
    ).first()

    if not rt:
        raise HTTPException(400, "This reset link is invalid or has expired. Please request a new one.")

    try:
        security.validate_password(data.new_password)
    except ValueError as exc:
        raise HTTPException(422, str(exc))

    rt.user.password_hash = security.hash_password(data.new_password)
    rt.used = True
    db.commit()
    return {"message": "Password updated successfully. You can now log in."}
