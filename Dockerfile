FROM python:3.11-slim

# Non-root user for security
RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# Install deps in a cacheable layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Persistent storage for the SQLite database
RUN mkdir -p /app/data && chown -R app:app /app

USER app

EXPOSE 8000

ENV DATABASE_URL=sqlite:///./data/lms.db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
