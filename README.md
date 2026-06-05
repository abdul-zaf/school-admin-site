# 🎓 EduPortal — School Learning Management System

A full-stack LMS built for schools, with bilingual support (English / اردو),
a full quiz and assignment workflow, AI-assisted learning tools, and one-click
deployment to Render.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | FastAPI · SQLAlchemy ORM · Pydantic v2 |
| Database | SQLite (dev) · PostgreSQL (production) |
| Auth | JWT (python-jose) · bcrypt (passlib) |
| Frontend | Vanilla JS SPA · CSS custom properties |
| PDF | ReportLab |
| CI | GitHub Actions (lint + pytest) |
| CD | GitHub Actions → Docker → GHCR → Render |

---

## Features

### Core LMS
- **Courses** — create, enrol, manage; subject colour-coding on cards
- **Materials** — text, links, file attachments per course
- **Assignments** — create, submit, grade with feedback; audit trail
- **Quizzes** — multiple choice, true/false, short answer; auto-grading; draft/publish workflow; per-quiz retake limits
- **Sessions** — virtual (meeting link) and in-person (room/location)
- **Announcements** — school-wide or per-course
- **Gradebook** — weighted categories, GPA, letter grades, drop-lowest
- **Calendar** — upcoming assignments, quizzes, sessions across all courses
- **Modules** — ordered lesson content with completion tracking

### Communication & Collaboration
- **Direct messages** — inbox / sent
- **Discussion boards** — per course, teacher-moderated
- **Anonymous help board** — Stack Overflow-style Q&A; teacher endorsement
- **Teach-it-back** — students explain concepts in their own words; peers upvote
- **Study group auto-matcher** — pairs students by complementary performance
- **Notifications** — in-app bell + email when a grade is posted

### Intelligence & Analytics
- **Spaced repetition** (SM-2) — flashcards auto-created from wrong quiz answers
- **Confusion heatmap** — students signal confusion during live sessions
- **Knowledge graph** — concept map with directional links; Canvas API visualisation
- **Analytics** — grade distribution, submission rates, active students

### Gamification & Recognition
- **Leaderboard** — per-course podium + school-wide top-25
- **Badges** — teachers award custom emoji badges
- **Portfolio** — students curate public work samples
- **Completion certificates** — auto-generated PDF when course is finished

### Admin & Security
- **Role-based access** — admin / teacher / student / parent
- **Password reset via email** — time-limited tokenised links
- **Dark mode** — saved per user
- **Bilingual UI** — English ↔ اردو with RTL layout
- **Rate limiting** — 10 login attempts / 60 s per IP
- **Timing-attack prevention** — dummy bcrypt hash on unknown emails
- **Course ownership guards** — teachers can only manage their own courses

---

## Quick start (local dev)

> **Prerequisite:** Install Python from [python.org](https://python.org/downloads) — during installation, tick **"Add Python to PATH"** before clicking Install.

**1. Clone the repo**
```bash
git clone https://github.com/abdul-zaf/school-admin-site.git
cd school-admin-site
```

**2. Create a virtual environment**
```bash
python -m venv venv
```

**3. Activate it**
```bash
# Windows
venv\Scripts\activate

# macOS / Linux / Git Bash
source venv/bin/activate
```
You should see `(venv)` at the start of your prompt.

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Start the server**
```bash
uvicorn main:app --reload
```

**6. Open your browser**
```
http://localhost:8000
```

Default admin credentials:
```
Email:    admin@school.edu
Password: Admin123
```

> Change the admin password immediately after first login.

**Next time** you only need steps 1 (navigate to folder), 3 (activate), and 5 (run) — the venv and dependencies are already set up.

### Interactive API docs
```
http://localhost:8000/api/docs
```

---

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | **Production** | random (warns) | JWT signing secret |
| `DATABASE_URL` | Optional | `sqlite:///./data/lms.db` | SQLAlchemy connection string |
| `ENVIRONMENT` | Optional | — | Set to `production` to enable HSTS |
| `ALLOWED_ORIGINS` | Optional | localhost + Render URL | CORS allowed origins (comma-separated) |
| `SMTP_HOST` | Optional | `smtp.gmail.com` | SMTP server for email |
| `SMTP_PORT` | Optional | `587` | SMTP port (STARTTLS) |
| `SMTP_USER` | Optional | — | Sending email address |
| `SMTP_PASSWORD` | Optional | — | SMTP / Gmail App Password |
| `FROM_EMAIL` | Optional | `SMTP_USER` | From address shown in emails |
| `APP_URL` | Optional | `RENDER_EXTERNAL_URL` | Base URL used in email links |

Without `SMTP_USER` / `SMTP_PASSWORD`, emails are printed to the console instead of being sent — useful for development.

---

## Running tests

```bash
pip install -r requirements-dev.txt
pytest                           # run all tests
pytest --cov=. --cov-report=term # with coverage
```

Tests use an isolated SQLite database (`test_lms.db`) and bypass rate limiting automatically via the `TESTING=1` environment variable.

---

## Deployment (Render)

The repo includes a `render.yaml` Blueprint — one-click deploy:

1. [render.com](https://render.com) → **New → Blueprint** → connect this repo
2. Render creates the web service + free PostgreSQL database automatically
3. `SECRET_KEY` is auto-generated as a managed secret
4. Service URL appears in ~3 minutes

### CI/CD pipeline

Every `git push` triggers:
```
CI (lint + test) → CD (Docker build → push to GHCR → trigger Render deploy)
```

To activate the CD deploy step, add `RENDER_DEPLOY_HOOK_URL` as a GitHub Actions secret (copy the Deploy Hook URL from the Render dashboard → Settings).

---

## Project structure

```
lms/
├── main.py                  # FastAPI app, middleware, router registration
├── database.py              # SQLAlchemy engine, session, migrations
├── models.py                # All ORM models (single file)
├── security.py              # JWT, bcrypt, rate limiter, course-access guard
│
├── routers/                 # One file per feature domain
│   ├── auth.py              # Login
│   ├── users.py             # User CRUD + CSV bulk import
│   ├── courses.py           # Courses, enrolment, materials, attendance
│   ├── assignments.py       # Assignments + submissions + grading
│   ├── quizzes.py           # Quiz builder, student attempt, auto-grading
│   ├── sessions.py          # Virtual / physical class sessions
│   ├── announcements.py     # School and course announcements
│   ├── gradebook.py         # Weighted gradebook, GPA, letter grades
│   ├── analytics.py         # Aggregate stats for teachers/admins
│   ├── leaderboard.py       # Course + school-wide rankings
│   ├── certificates.py      # PDF completion certificates (ReportLab)
│   ├── password_reset.py    # Forgot-password email flow
│   ├── messages.py          # Direct messaging
│   ├── notifications.py     # In-app notifications
│   ├── discussions.py       # Per-course discussion boards
│   ├── badges.py            # Achievement badges
│   ├── portfolio.py         # Student portfolios
│   ├── modules.py           # Course modules with completion tracking
│   ├── question_banks.py    # Reusable question pools
│   ├── rubrics.py           # Rubric-based grading
│   ├── surveys.py           # Teacher-created surveys
│   ├── parents.py           # Parent–student links
│   ├── spaced_repetition.py # SM-2 flashcard system
│   ├── teach_back.py        # Student concept explanations + peer votes
│   ├── confusion.py         # Live confusion signals during sessions
│   ├── help_board.py        # Anonymous course Q&A board
│   ├── knowledge_graph.py   # Concept map with Canvas visualisation
│   └── study_groups.py      # Auto-matched study groups
│
├── services/
│   └── email.py             # Shared SMTP email helper + notification templates
│
├── static/
│   ├── index.html           # Single HTML shell (login + app layout)
│   ├── app.js               # SPA core: routing, auth, all page renderers
│   ├── features.js          # Extended features: SR, teach-back, help board, etc.
│   └── style.css            # Design system (CSS custom properties, dark mode)
│
├── tests/
│   ├── conftest.py          # pytest fixtures, isolated DB setup
│   └── test_security.py     # Auth, ownership, rate-limiting tests
│
├── Dockerfile               # python:3.11-slim, non-root user, $PORT support
├── render.yaml              # Render Blueprint (web service + Postgres)
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Dev/test dependencies (pytest, ruff, httpx)
└── ruff.toml                # Linter config
```

---

## Adding a new feature

1. **Model** — add your table class to `models.py`
2. **Migration** — add an `ALTER TABLE … ADD COLUMN IF NOT EXISTS` statement to `apply_migrations()` in `database.py` (for new columns on existing tables only; new tables are handled by `create_all`)
3. **Router** — create `routers/my_feature.py` with a module docstring and an `APIRouter`
4. **Register** — import and `app.include_router(...)` in `main.py`
5. **Frontend** — add i18n keys to both `en` and `ur` objects in `app.js`, add a render function, wire it into `navigate()`
6. **Tests** — add test cases to `tests/`

---

## License

MIT — free to use, modify, and deploy for educational purposes.
