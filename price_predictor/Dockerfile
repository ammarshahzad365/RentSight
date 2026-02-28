FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code and model artifacts
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --no-create-home appuser
USER appuser

# Render injects PORT env var (default 10000)
EXPOSE ${PORT:-10000}

CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000} --log-level info
