import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lms.db")

# Render (and some other PaaS) prefix Postgres URLs with "postgres://" which
# SQLAlchemy 1.4+ requires to be "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

_is_sqlite = DATABASE_URL.startswith("sqlite")

# check_same_thread is SQLite-only; pool_pre_ping keeps Postgres connections
# alive across the idle periods common on free-tier dynos.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if _is_sqlite else {},
    pool_pre_ping=not _is_sqlite,   # SQLite doesn't need / support this
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def apply_migrations():
    """Lightweight schema migrations so existing DBs gain new columns without data loss.

    Each DDL runs in its own begin()/commit() so a failed ALTER TABLE (column
    already exists) does NOT leave the connection in a dirty state that would
    corrupt subsequent operations on the same pooled connection.
    """
    ddl_list_sqlite = [
        # v2: quiz publish flag + retake limit
        "ALTER TABLE quizzes ADD COLUMN is_published BOOLEAN NOT NULL DEFAULT 0",
        "ALTER TABLE quizzes ADD COLUMN max_attempts INTEGER",
        # v3: material file upload
        "ALTER TABLE materials ADD COLUMN material_type TEXT NOT NULL DEFAULT 'text'",
        "ALTER TABLE materials ADD COLUMN file_name TEXT",
        "ALTER TABLE materials ADD COLUMN file_path TEXT",
        "ALTER TABLE materials ADD COLUMN file_size INTEGER",
        "ALTER TABLE materials ADD COLUMN file_mime TEXT",
        # v4: assignment gradebook + rubric columns
        "ALTER TABLE assignments ADD COLUMN grade_category_id INTEGER REFERENCES grade_categories(id)",
        "ALTER TABLE assignments ADD COLUMN is_extra_credit BOOLEAN NOT NULL DEFAULT 0",
        "ALTER TABLE assignments ADD COLUMN rubric_id INTEGER REFERENCES rubrics(id)",
        # v5: late submission + resubmission policy
        "ALTER TABLE assignments ADD COLUMN late_penalty_per_day REAL NOT NULL DEFAULT 0",
        "ALTER TABLE assignments ADD COLUMN max_late_days INTEGER",
        "ALTER TABLE assignments ADD COLUMN allow_resubmission BOOLEAN NOT NULL DEFAULT 0",
        "ALTER TABLE assignments ADD COLUMN max_submissions INTEGER NOT NULL DEFAULT 1",
        # v5: announcement scheduling
        "ALTER TABLE announcements ADD COLUMN publish_at DATETIME",
        # v5: enrollment cap
        "ALTER TABLE courses ADD COLUMN enrollment_cap INTEGER",
        # v5: user email notification preference
        "ALTER TABLE users ADD COLUMN email_notifications BOOLEAN NOT NULL DEFAULT 1",
        # v6: AI tutor session mode + assignment context
        "ALTER TABLE tutor_sessions ADD COLUMN mode TEXT NOT NULL DEFAULT 'study'",
        "ALTER TABLE tutor_sessions ADD COLUMN assignment_id INTEGER REFERENCES assignments(id)",
        # v7: AI tutor cross-session memory (summary injection)
        "ALTER TABLE tutor_sessions ADD COLUMN summary TEXT",
        "ALTER TABLE tutor_sessions ADD COLUMN summarized_at DATETIME",
    ]

    if _is_sqlite:
        # Each statement in its own transaction so a failure (duplicate column)
        # leaves the connection clean for the next statement.
        for ddl in ddl_list_sqlite:
            try:
                with engine.begin() as conn:
                    conn.execute(text(ddl))
            except Exception:
                pass  # column already exists — safe to ignore
    else:
        # Postgres supports IF NOT EXISTS so all can run in one transaction
        with engine.begin() as conn:
            for ddl in [
                # v2
                "ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS is_published BOOLEAN NOT NULL DEFAULT FALSE",
                "ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS max_attempts INTEGER",
                # v3
                "ALTER TABLE materials ADD COLUMN IF NOT EXISTS material_type VARCHAR(20) NOT NULL DEFAULT 'text'",
                "ALTER TABLE materials ADD COLUMN IF NOT EXISTS file_name VARCHAR(300)",
                "ALTER TABLE materials ADD COLUMN IF NOT EXISTS file_path VARCHAR(500)",
                "ALTER TABLE materials ADD COLUMN IF NOT EXISTS file_size INTEGER",
                "ALTER TABLE materials ADD COLUMN IF NOT EXISTS file_mime VARCHAR(100)",
                # v4
                "ALTER TABLE assignments ADD COLUMN IF NOT EXISTS grade_category_id INTEGER REFERENCES grade_categories(id)",
                "ALTER TABLE assignments ADD COLUMN IF NOT EXISTS is_extra_credit BOOLEAN NOT NULL DEFAULT FALSE",
                "ALTER TABLE assignments ADD COLUMN IF NOT EXISTS rubric_id INTEGER REFERENCES rubrics(id)",
                # v5
                "ALTER TABLE assignments ADD COLUMN IF NOT EXISTS late_penalty_per_day FLOAT NOT NULL DEFAULT 0",
                "ALTER TABLE assignments ADD COLUMN IF NOT EXISTS max_late_days INTEGER",
                "ALTER TABLE assignments ADD COLUMN IF NOT EXISTS allow_resubmission BOOLEAN NOT NULL DEFAULT FALSE",
                "ALTER TABLE assignments ADD COLUMN IF NOT EXISTS max_submissions INTEGER NOT NULL DEFAULT 1",
                "ALTER TABLE announcements ADD COLUMN IF NOT EXISTS publish_at TIMESTAMP",
                "ALTER TABLE courses ADD COLUMN IF NOT EXISTS enrollment_cap INTEGER",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_notifications BOOLEAN NOT NULL DEFAULT TRUE",
                # v6: AI tutor session mode + assignment context
                "ALTER TABLE tutor_sessions ADD COLUMN IF NOT EXISTS mode VARCHAR(20) NOT NULL DEFAULT 'study'",
                "ALTER TABLE tutor_sessions ADD COLUMN IF NOT EXISTS assignment_id INTEGER REFERENCES assignments(id)",
                # v7: AI tutor cross-session memory (summary injection)
                "ALTER TABLE tutor_sessions ADD COLUMN IF NOT EXISTS summary TEXT",
                "ALTER TABLE tutor_sessions ADD COLUMN IF NOT EXISTS summarized_at TIMESTAMP",
            ]:
                conn.execute(text(ddl))
