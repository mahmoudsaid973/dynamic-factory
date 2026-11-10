FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv sync --no-dev --no-cache

FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY --from=builder /app/.venv /app/.venv
COPY src ./src

USER appuser

EXPOSE 8000

CMD ["uvicorn", "dynamic_factory.main:app", "--host", "0.0.0.0", "--port", "8000"]
