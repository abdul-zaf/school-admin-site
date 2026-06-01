# EduPortal — Claude Code Context

This file gives Claude Code the project-specific context needed to work
effectively on this codebase without re-deriving it from scratch each session.

---

## Architecture in one paragraph

EduPortal is a **FastAPI + SQLite/PostgreSQL monolith** that serves a
**vanilla-JS SPA** from the same process. There is no separate frontend build
step — `static/index.html` is served at `/`, and `static/app.js` handles all
routing, API calls, and DOM rendering. Authentication is JWT Bearer (24 h
tokens). Every API route lives under `/api/`. The database layer is plain
SQLAlchemy ORM (no Alembic — schema changes go through `apply_migrations()` in
`database.py`).

---

## Key files

| File | Role |
|---|---|
| `main.py` | App factory — imports all routers, registers middleware, seeds admin |
| `database.py` | Engine, `get_db()` dependency, `apply_migrations()` |
| `models.py` | **All** ORM models in one file |
| `security.py` | JWT, bcrypt, rate limiter, `require_role()`, `require_course_access()` |
| `static/app.js` | SPA core: i18n, state, API helper, page renderers, navigation |
| `static/features.js` | Extended feature renderers (SR, teach-back, knowledge graph, etc.) |
| `static/style.css` | CSS custom properties; `[data-theme="dark"]` overrides at bottom |

---

## Database conventions

- **All models in `models.py`** — one file, imports are simple.
- **New tables** are created automatically by `Base.metadata.create_all(bind=engine)` on startup.
- **New columns on existing tables** must be added to `apply_migrations()` in `database.py`:

```python
# SQLite (no IF NOT EXISTS on ALTER TABLE)
try:
    conn.execute(text("ALTER TABLE foo ADD COLUMN bar INTEGER"))
    conn.commit()
except Exception:
    pass  # column already exists

# PostgreSQL (supports IF NOT EXISTS)
conn.execute(text("ALTER TABLE foo ADD COLUMN IF NOT EXISTS bar INTEGER"))
conn.commit()
```

The function is dialect-aware — check the `_is_sqlite` flag at the top.

- **Foreign keys** use `ForeignKey("table.id")` strings, not model references.
- **Relationships** are defined on the model that "owns" the data. Cascades are
  set explicitly (`cascade="all, delete"`) on owned relationships.
- **Boolean columns** use `default=False, nullable=False` unless nullable is
  intentional.

---

## Auth patterns

### Protect an endpoint (role check)

```python
from security import require_role

@router.get("/admin-only")
def my_endpoint(
    current_user: models.User = Depends(require_role("admin")),
):
    ...

# Multiple roles
@router.post("/teacher-or-admin")
def create_thing(
    current_user: models.User = Depends(require_role("admin", "teacher")),
):
    ...
```

### Any authenticated user

```python
from security import get_current_user

@router.get("/my-data")
def get_data(
    current_user: models.User = Depends(get_current_user),
):
    ...
```

### Course ownership guard

```python
from security import require_course_access

# Returns the course or raises 403/404
course = security.require_course_access(course_id, current_user, db)
```

Use this on any endpoint where a teacher is modifying course content.
It allows admins through and blocks teachers from touching other teachers' courses.

---

## Adding a new router

1. Create `routers/my_feature.py` — start with a module docstring and `router = APIRouter()`
2. In `main.py`:
   - Import: `from routers import ..., my_feature`
   - Register: `app.include_router(my_feature.router, prefix="/api/my-feature", tags=["my-feature"])`
3. If new models are needed, add them to `models.py` (new tables need no migration)
4. If adding columns to existing tables, update `apply_migrations()` in `database.py`

---

## Frontend SPA patterns

### Navigation

```javascript
navigate('my_page', { param: 123 });
```

Add a branch in the `navigate()` function in `app.js`:
```javascript
else if (page === 'my_page') renderMyPage(params.param, el);
```

Add to `NAV_KEYS` for the relevant roles, `NAV_ICONS` for the emoji, and `NAV_I18N` for the translation key.

### i18n

Always add keys to **both** `i18n.en` and `i18n.ur`:
```javascript
// in i18n.en
my_key: 'English text',

// in i18n.ur
my_key: 'اردو متن',
```

Use `t('my_key')` anywhere in a template literal. The `t()` function falls back
to English if the Urdu key is missing.

### API calls

```javascript
const data = await api('GET', '/my-feature/123');
await api('POST', '/my-feature', { title: 'hello' });
await api('DELETE', `/my-feature/${id}`);
```

`api()` automatically attaches the Bearer token and throws on non-2xx responses.
It calls `logout()` on 401 (expired token).

### Rendering pattern

```javascript
async function renderMyPage(el) {
  loading(el);              // shows spinner
  try {
    const data = await api('GET', '/my-feature');
    el.innerHTML = `...`;   // set content
  } catch(err) {
    el.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
  }
}
```

---

## Email (shared helper)

```python
from services.email import send_email, send_grade_notification

# Generic
send_email(to_email, to_name, subject, html_body, plain_body)

# Grade notification (pre-built template)
send_grade_notification(to_email, to_name, assignment_title,
                        course_title, score, max_score, feedback, app_url)
```

Both are safe to call from a FastAPI `BackgroundTasks` task.
If `SMTP_USER` / `SMTP_PASSWORD` are unset, the message is printed to stdout
instead — no crash, no silent failure.

---

## CSS design tokens

```css
/* Light mode (default) */
--bg, --card, --border, --text, --muted   /* surface colours */
--indigo, --gold, --success, --warning, --danger, --info   /* brand/status */
--sb-bg, --sb-mid   /* sidebar gradient */
--accent   /* overridden per course card via inline style */

/* Dark mode: set [data-theme="dark"] on <html> */
/* All overrides are at the bottom of style.css */
```

Subject-to-colour mapping for course cards is in `subjectAccent()` in `app.js`.

---

## Testing

```bash
pytest                        # all tests
pytest tests/test_security.py # specific file
pytest -k "test_login"        # specific test
```

- **Fixtures** are in `tests/conftest.py`.
- Each test gets a **fresh database** — the `autouse` fixture drops and recreates
  all tables before every test.
- `TESTING=1` is set automatically, which bypasses rate limiting.
- Test password: `"testPass1"` (meets policy: ≥ 8 chars, letter + digit).
- Headers: `admin_h`, `teacher_h`, `student_h` fixtures return auth headers.

---

## Common gotchas

| Situation | Fix |
|---|---|
| New column not appearing | Add to `apply_migrations()` AND the model |
| `check_same_thread` error | Only for SQLite — the `_is_sqlite` flag in `database.py` handles this |
| Postgres URL starts with `postgres://` | `database.py` rewrites it to `postgresql://` automatically |
| Rate limiter blocking tests | Set `TESTING=1` or use the existing pytest fixture |
| Password validation failing in tests | Use `"testPass1"` (has letter + digit + 8 chars) |
| CORS errors on Render | `RENDER_EXTERNAL_URL` is auto-detected; set `ALLOWED_ORIGINS` for custom domains |
| Urdu text misaligned | Wrapped elements need `[dir="rtl"]` CSS selectors — see bottom of `style.css` |
