# ======================================
# Stage 1 - Base image with common setup
# ======================================
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# ==================================
# Stage 2 - Download ephemeris files
# ==================================
FROM base AS ephe

ENV EPHE_BASE_URL=https://github.com/aloistr/swisseph/raw/master/ephe

RUN mkdir -p /app/ephe && \
    curl -fsSL -o /app/ephe/sepl_18.se1 ${EPHE_BASE_URL}/sepl_18.se1 && \
    curl -fsSL -o /app/ephe/semo_18.se1 ${EPHE_BASE_URL}/semo_18.se1 && \
    curl -fsSL -o /app/ephe/seas_18.se1 ${EPHE_BASE_URL}/seas_18.se1

# ==============================
# Stage 3 - Install dependencies
# ==============================
FROM base AS deps

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-cache

# =======================
# Stage 4 - Runtime image
# =======================
FROM base AS runtime

RUN useradd -m -u 10001 appuser

ENV EPHE_PATH=/app/ephe

# Copy ephemeris files from dedicated stage
COPY --from=ephe /app/ephe /app/ephe

# Copy installed virtual environment
COPY --from=deps /app/.venv /app/.venv

# Copy application source code
COPY app/ ./app/

RUN chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "app.main"]
