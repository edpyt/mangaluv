FROM python:3.13-bullseye AS base
COPY --from=ghcr.io/astral-sh/uv:0.8.2 /uv /uvx /bin/
ENV UV_PROJECT_ENVIRONMENT=/usr/local
COPY . /app
WORKDIR /app

FROM base AS run
RUN uv sync --frozen --no-cache
CMD ["uvicorn", "--factory", "src.auth_service.main:create_production_app", \
  "--port", "80", "--host", "0.0.0.0"]

FROM base AS migrations
RUN uv sync --frozen --no-cache --only-group migrations 
CMD ["alembic", "upgrade", "head"]
