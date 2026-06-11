"""
Shared email helper used by grade notifications, due-date reminders, etc.
SMTP credentials are read from environment variables:
  SMTP_HOST     (default: smtp.gmail.com)
  SMTP_PORT     (default: 587)
  SMTP_USER     your sending address
  SMTP_PASSWORD Gmail App Password or SMTP password
  FROM_EMAIL    optional — defaults to SMTP_USER
If SMTP_USER / SMTP_PASSWORD are absent the message is printed to the console
instead, so local development works without an email account.
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _smtp_cfg():
    return {
        "host":     os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "port":     int(os.getenv("SMTP_PORT", "587")),
        "user":     os.getenv("SMTP_USER", ""),
        "password": os.getenv("SMTP_PASSWORD", ""),
        "from":     os.getenv("FROM_EMAIL", os.getenv("SMTP_USER", "noreply@school.edu")),
    }


def send_email(
    to_email: str,
    to_name: str,
    subject: str,
    html_body: str,
    plain_body: str = "",
) -> None:
    """Send an HTML email.  Safe to call from a BackgroundTask thread."""
    cfg = _smtp_cfg()
    if not cfg["user"] or not cfg["password"]:
        sep = "-" * 60
        print(
            f"\n{sep}\n"
            f"[EMAIL] SMTP not configured - printing instead.\n"
            f"To: {to_email}\nSubject: {subject}\n{plain_body or '(html only)'}\n"
            f"{sep}\n"
        )
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"EduPortal <{cfg['from']}>"
    msg["To"]      = to_email
    if plain_body:
        msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(cfg["host"], cfg["port"]) as srv:
            srv.ehlo()
            srv.starttls()
            srv.login(cfg["user"], cfg["password"])
            srv.sendmail(cfg["from"], to_email, msg.as_string())
        print(f"[EMAIL] Sent '{subject}' → {to_email}")
    except Exception as exc:
        print(f"[EMAIL] Failed → {to_email}: {exc}")


# ── Pre-built notification templates ─────────────────────────────────────────

def _wrap(body_inner: str) -> str:
    return f"""
    <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px">
      <div style="background:linear-gradient(135deg,#1e1b4b,#4f46e5);
                  padding:24px;border-radius:12px 12px 0 0;text-align:center">
        <h1 style="color:#fff;margin:0;font-size:24px">EduPortal</h1>
      </div>
      <div style="background:#fff;padding:28px;border:1px solid #e0e7ff;
                  border-top:none;border-radius:0 0 12px 12px">
        {body_inner}
        <hr style="border:none;border-top:1px solid #e0e7ff;margin:20px 0">
        <p style="color:#9ca3af;font-size:11px;margin:0">
          EduPortal School LMS — this is an automated message.
        </p>
      </div>
    </body></html>
    """


def send_grade_notification(
    to_email: str,
    to_name: str,
    assignment_title: str,
    course_title: str,
    score: float,
    max_score: float,
    feedback: str | None,
    app_url: str = "",
) -> None:
    pct   = round(score / max_score * 100) if max_score else 0
    color = "#059669" if pct >= 70 else "#d97706" if pct >= 50 else "#e11d48"
    fb    = f"<p style='color:#374151'><strong>Feedback:</strong> {feedback}</p>" if feedback else ""
    html  = _wrap(f"""
        <h2 style="color:#1e1b4b;margin-top:0">Your assignment has been graded</h2>
        <p style="color:#374151">Hi <strong>{to_name}</strong>,</p>
        <p style="color:#374151">
          Your submission for <strong>{assignment_title}</strong>
          in <em>{course_title}</em> has been graded.
        </p>
        <div style="text-align:center;margin:24px 0;padding:20px;
                    background:#f9fafb;border-radius:10px">
          <span style="font-size:48px;font-weight:800;color:{color}">
            {score}/{max_score}
          </span>
          <p style="color:{color};font-weight:700;font-size:18px;margin:4px 0">{pct}%</p>
        </div>
        {fb}
        {f'<p><a href="{app_url}" style="color:#4f46e5">Open EduPortal</a></p>' if app_url else ""}
    """)
    plain = (
        f"Hi {to_name},\n\n"
        f"Your assignment '{assignment_title}' in {course_title} has been graded.\n"
        f"Score: {score}/{max_score} ({pct}%)\n"
        f"{('Feedback: ' + feedback) if feedback else ''}\n"
    )
    send_email(to_email, to_name, f"Grade posted - {assignment_title}", html, plain)


def notify_new_announcement(to_email: str, to_name: str, course_title: str, announcement_title: str) -> None:
    html = _wrap(f"""
        <h2 style="color:#1e1b4b;margin-top:0">New Announcement</h2>
        <p style="color:#374151">Hi <strong>{to_name}</strong>,</p>
        <p style="color:#374151">A new announcement <strong>{announcement_title}</strong>
        has been posted in <em>{course_title}</em>.</p>
    """)
    send_email(to_email, to_name, f"[LMS] New announcement: {announcement_title}", html)


def notify_password_reset(to_email: str, to_name: str, reset_link: str) -> None:
    html = _wrap(f"""
        <h2 style="color:#1e1b4b;margin-top:0">Password Reset Request</h2>
        <p style="color:#374151">Hi <strong>{to_name}</strong>,</p>
        <p style="color:#374151">Click <a href="{reset_link}" style="color:#4f46e5">here</a>
        to reset your password. This link expires in 1 hour.</p>
        <p style="color:#374151">If you did not request this, please ignore this email.</p>
    """)
    send_email(to_email, to_name, "[LMS] Password Reset Request", html)
