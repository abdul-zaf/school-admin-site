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
        # v2: quiz publish flag
        if _is_sqlite:
            for ddl in [
                "ALTER TABLE quizzes ADD COLUMN is_published BOOLEAN NOT NULL DEFAULT 0",
                "ALTER TABLE quizzes ADD COLUMN max_attempts INTEGER",
            ]:
                try:
                    conn.execute(text(ddl))
                    conn.commit()
                except Exception:
                    pass  # column already exists — safe to ignore
        else:
            conn.execute(text(
                "ALTER TABLE quizzes "
                "ADD COLUMN IF NOT EXISTS is_published BOOLEAN NOT NULL DEFAULT FALSE"
            ))
            conn.execute(text(
                "ALTER TABLE quizzes "
                "ADD COLUMN IF NOT EXISTS max_attempts INTEGER"
            ))
            conn.commit()
