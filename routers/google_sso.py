"""
Google OAuth 2.0 Sign-In.

Required environment variables:
  GOOGLE_CLIENT_ID       from Google Cloud Console
  GOOGLE_CLIENT_SECRET   from Google Cloud Console

Setup (one-time, free):
  1. console.cloud.google.com → Create project → APIs & Services → Credentials
  2. Create OAuth 2.0 Client ID  (type: Web application)
  3. Add Authorised redirect URI:
       http://localhost:8000/api/auth/google/callback   (local dev)
       https://your-app.onrender.com/api/auth/google/callback  (production)
  4. Copy Client ID + Client Secret into env vars above.

Flow:
  GET  /api/auth/google            → redirects browser to Google consent screen
  GET  /api/auth/google/callback   → exchanges code, finds/creates user, redirects
                                     to /?sso_token=JWT&name=NAME&role=ROLE&user_id=ID

  The frontend detects ?sso_token in the URL and auto-logs the user in.
"""
import json
import os
import secrets
import urllib.parse
import urllib.request

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
import models
import security

router = APIRouter()

_GOOGLE_AUTH_URL  = "https://accounts.google.com/o/oauth2/v2/auth"
_GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
_GOOGLE_INFO_URL  = "https://www.googleapis.com/oauth2/v3/userinfo"


def _app_url() -> str:
    return (
        os.getenv("APP_URL")
        or os.getenv("RENDER_EXTERNAL_URL", "")
        or "http://localhost:8000"
    ).rstrip("/")


def _redirect_uri() -> str:
    return f"{_app_url()}/api/auth/google/callback"


def _cfg():
    return {
        "client_id":     os.getenv("GOOGLE_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
    }


@router.get("/google")
def google_login():
    cfg = _cfg()
    if not cfg["client_id"]:
        raise HTTPException(501, "Google SSO is not configured on this server.")

    params = {
        "client_id":     cfg["client_id"],
        "redirect_uri":  _redirect_uri(),
        "response_type": "code",
        "scope":         "openid email profile",
        "access_type":   "online",
        "prompt":        "select_account",
    }
    url = f"{_GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


@router.get("/google/callback")
def google_callback(code: str = "", error: str = "", db: Session = Depends(get_db)):
    if error or not code:
        return RedirectResponse(f"{_app_url()}/?sso_error=access_denied")

    cfg = _cfg()

    # ── Exchange code for access token ──
    token_data = urllib.parse.urlencode({
        "code":          code,
        "client_id":     cfg["client_id"],
        "client_secret": cfg["client_secret"],
        "redirect_uri":  _redirect_uri(),
        "grant_type":    "authorization_code",
    }).encode()

    try:
        req = urllib.request.Request(
            _GOOGLE_TOKEN_URL,
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            token_json = json.loads(resp.read())
    except Exception as exc:
        print(f"[Google SSO] Token exchange failed: {exc}")
        return RedirectResponse(f"{_app_url()}/?sso_error=token_failed")

    access_token = token_json.get("access_token", "")
    if not access_token:
        return RedirectResponse(f"{_app_url()}/?sso_error=no_token")

    # ── Fetch user info ──
    try:
        req = urllib.request.Request(
            _GOOGLE_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            info = json.loads(resp.read())
    except Exception as exc:
        print(f"[Google SSO] User info failed: {exc}")
        return RedirectResponse(f"{_app_url()}/?sso_error=info_failed")

    email = info.get("email", "").lower().strip()
    name  = info.get("name") or email.split("@")[0]

    if not email:
        return RedirectResponse(f"{_app_url()}/?sso_error=no_email")

    # ── Find or create user ──
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            name          = name,
            email         = email,
            password_hash = security.hash_password(secrets.token_urlsafe(32)),
            role          = "student",   # default role for new SSO accounts
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"[Google SSO] Created new user: {email}")
    else:
        print(f"[Google SSO] Existing user logged in: {email}")

    # ── Issue JWT (same 24-hour token as normal login) ──
    token = security.create_token(user.id)

    # ── Redirect to frontend with token in URL params ──
    params = urllib.parse.urlencode({
        "sso_token": token,
        "user_id":   user.id,
        "name":      user.name,
        "role":      user.role,
    })
    return RedirectResponse(f"{_app_url()}/?{params}")
