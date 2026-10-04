dev:
  uv run uvicorn dangerous_api.cmd.api:app --reload

start:
  uv run uvicorn dangerous_api.cmd.api:app

collector:
  uv run python -m dangerous_api.cmd.collector

test:
  uv run pytest

format:
  uv run ruff format .

lint:
  uv run ruff check .

# --- database ---
db-up:
  docker run -d --name dangerous-db -e POSTGRES_USER=dangerous -e POSTGRES_PASSWORD=dangerous \
    -e POSTGRES_DB=dangerous -p 5432:5432 -v dangerous-pgdata:/var/lib/postgresql/data postgres:17

db-down:
  docker rm -f dangerous-db

# usage: just revision "add commanders table"
revision msg:
  uv run alembic revision --autogenerate -m "{{msg}}"

migrate:
  uv run alembic upgrade head

rollback:
  uv run alembic downgrade -1
