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
    finally:
        db.close()

def apply_migrations():
    """Lightweight schema migrations so existing DBs gain new columns without data loss."""
    with engine.connect() as conn:
        if _is_sqlite:
            for ddl in [
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
            ]:
                try:
                    conn.execute(text(ddl))
                    conn.commit()
                except Exception:
                    pass  # column already exists — safe to ignore
        else:
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
            ]:
                conn.execute(text(ddl))
            conn.commit()
