dev:
  uv run uvicorn inara.cmd.api:app --reload
start:
  uv run uvicorn inara.cmd.api:app
test:
  uv run pytest
format:
  uv run ruff format .
lint:
  uv run ruff check .
