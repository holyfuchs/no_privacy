FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

COPY . .
EXPOSE 8000

CMD ["uv", "run", "--no-dev", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]
