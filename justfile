dev:
  uv run uvicorn inara.cmd.api:app --reload

start:
  uv run uvicorn inara.cmd.api:app

collector:
  uv run python -m inara.cmd.collector

test:
  uv run pytest

format:
  uv run ruff format .

lint:
  uv run ruff check .

# --- database ---
db-up:
  docker run -d --name inara-db -e POSTGRES_USER=inara -e POSTGRES_PASSWORD=inara \
    -e POSTGRES_DB=inara -p 5432:5432 postgres:17

db-down:
  docker rm -f inara-db

# usage: just revision "add commanders table"
revision msg:
  uv run alembic revision --autogenerate -m "{{msg}}"

migrate:
  uv run alembic upgrade head

rollback:
  uv run alembic downgrade -1
