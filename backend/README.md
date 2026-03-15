# StockPulse Backend

FastAPI backend for the StockPulse AI-Powered Stock Tracking & Insights Platform.

## Requirements

- Python 3.12+
- PostgreSQL 15+ (or SQLite for local dev)
- Redis 7+ (optional for dev — caching layer)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Quick Start

```bash
# 1. Clone and enter the backend directory
cd backend

# 2. Install dependencies
uv pip install -e ".[dev]"

# 3. Copy and configure environment
cp .env.example .env
# Edit .env — set DATABASE_URL, SECRET_KEY, ANTHROPIC_API_KEY, etc.

# 4. Run database migrations
alembic upgrade head

# 5. Start the development server
uvicorn app.main:app --reload --port 8000
```

API docs are available at `http://localhost:8000/docs` when `APP_ENV=development`.

## Running Tests

```bash
pytest
```

## Linting & Type Checking

```bash
ruff check .
ruff format --check .
mypy app/
```

## Database Migrations

```bash
# Auto-generate a new migration after modifying models
alembic revision --autogenerate -m "describe the change"

# Apply all pending migrations
alembic upgrade head

# Roll back one step
alembic downgrade -1
```

Always review auto-generated migrations before committing — Alembic can miss column renames
or generate destructive operations.

## Project Structure

See `agents/BACKEND_AGENT.md` for full architecture documentation.

## Environment Variables

See `.env.example` for all required and optional variables with descriptions.
