FROM python:3.13-bullseye
COPY --from=ghcr.io/astral-sh/uv:0.8.2 /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["/app/.venv/bin/fastapi", "run", "/app/src/api_gateway/__init__.py", \
  "--port", "80", "--host", "0.0.0.0"]
