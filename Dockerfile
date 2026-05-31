FROM python:3.11-slim

# Non-root user for security
RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# Stream logs immediately (important on Render / cloud platforms)
ENV PYTHONUNBUFFERED=1

# Install deps in a cacheable layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Persistent storage directory for local SQLite runs.
# On Render this folder is unused — Postgres is injected via DATABASE_URL.
RUN mkdir -p /app/data && chown -R app:app /app

USER app

EXPOSE 8000

# Default to SQLite when no DATABASE_URL is provided (local dev / Docker desktop).
# Render overrides DATABASE_URL with its Postgres connection string automatically.
ENV DATABASE_URL=sqlite:///./data/lms.db

# Use shell form so ${PORT:-8000} expands at runtime.
# Render injects $PORT; every other environment falls back to 8000.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
