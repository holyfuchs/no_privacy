FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

COPY . .
EXPOSE 4321

CMD ["uv", "run", "--no-dev", "uvicorn", "main:app"]
