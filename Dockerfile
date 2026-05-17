# ======================================
# Stage 1 - Base image with common setup
# ======================================
FROM python:3.12-slim AS base

# Python + UV runtime settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# ==============================
# Stage 2 - Install dependencies
# ==============================
FROM base AS deps

# Copy dependency files separately for better layer caching
COPY pyproject.toml uv.lock ./

# Create virtual environment and install production deps
RUN uv sync --frozen --no-dev --no-cache

# =======================
# Stage 3 - Runtime image
# =======================
FROM base AS runtime

# Create non-root user
RUN useradd -m -u 10001 appuser

# Swiss Ephemeris data path
ENV EPHE_PATH=/app/ephe

# Create ephemeris directory
RUN mkdir -p /app/ephe

# Copy installed virtual environment
COPY --from=deps /app/.venv /app/.venv

# Copy application source code
COPY . .

# Set proper ownership
RUN chown -R appuser:appuser /app

# Run container as non-root user
USER appuser

EXPOSE 8000

# =========================
# Start FastAPI application
# =========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
