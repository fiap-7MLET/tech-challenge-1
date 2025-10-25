# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI-based REST API for book catalog management with web scraping functionality. Developed as FIAP ML Engineering Tech Challenge Phase 1. The system scrapes ~1000 books from books.toscrape.com, stores them in SQLite, and exposes RESTful endpoints.

## Development Commands

### Environment Setup
```bash
# Install dependencies (uses uv package manager)
uv sync

# Activate virtual environment (optional)
source .venv/bin/activate
```

### Running the Application
```bash
# Start development server with hot reload
uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# Access points:
# - API: http://localhost:8000
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage report (generates html/ directory)
uv run pytest --cov=src --cov-report=html

# Run single test file
uv run pytest tests/test_app.py

# Run single test function
uv run pytest tests/test_app.py::test_function_name
```

### Database Migrations (Alembic)
```bash
# Create new migration
uv run alembic revision -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# View migration history
uv run alembic history
```

### Web Scraping
```bash
# Trigger scraping process (populates database)
curl -X POST http://localhost:8000/scraping/trigger

# Check scraping status
curl http://localhost:8000/scraping/status
```

## Architecture

### Technology Stack
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM with declarative base pattern
- **Alembic**: Database migrations
- **httpx + BeautifulSoup4**: Async web scraping
- **Pydantic**: Schema validation
- **uv**: Package manager (NOT pip/poetry)

### Directory Structure
```
src/
├── app.py                  # FastAPI app initialization, router registration
├── extensions.py           # Database engine, SessionLocal, get_db() dependency
├── conf.py                 # Configuration settings
├── models/
│   ├── __init__.py        # Shared SQLAlchemy Base (declarative_base)
│   ├── book.py            # Book model
│   └── user.py            # User model
├── routes/                 # API endpoint routers (book, category, health, scraping, etc.)
├── api/schemas/           # Pydantic schemas for request/response validation
└── services/scraping/     # Async scraping logic and CSV file handling

migrations/
├── env.py                 # Alembic environment (loads models, dotenv)
└── versions/              # Migration files

tests/                     # Pytest tests with conftest.py fixtures
```

### Key Architectural Patterns

**Database Setup**:
- `src/models/__init__.py` exports shared `Base = declarative_base()`
- All models inherit from this Base to avoid table duplication
- `src/extensions.py` creates engine and SessionLocal from `DATABASE_URL` env var
- `get_db()` dependency provides scoped sessions to routes

**Migration System**:
- `migrations/env.py` imports all models explicitly (User, Book)
- Uses `target_metadata = Base.metadata` for auto-detection
- Loads DATABASE_URL from .env file via dotenv
- Add `src/` to sys.path for imports to work

**Router Registration**:
- All routers registered in `src/app.py` via `app.include_router()`
- Routes are modular, each in separate file under `src/routes/`

**Web Scraping**:
- Async implementation using httpx.AsyncClient
- Scrapes books.toscrape.com catalog
- Dual output: SQLite database + CSV file in `data/`
- Rating conversion: "One"→1, "Two"→2, etc.

## Environment Variables

Required `.env` file in project root:
```env
DATABASE_URL=sqlite:///db.sqlite3
DEBUG=False
```

## Important Implementation Notes

### Adding New Models
1. Create model file in `src/models/` inheriting from `Base`
2. Import model explicitly in `migrations/env.py` (add to imports section)
3. Run `uv run alembic revision -m "add model_name"`
4. Apply migration: `uv run alembic upgrade head`

### Import Consistency
- Always use `from src.models import Base` (NOT `from models import Base`)
- Inconsistent imports cause SQLAlchemy to create duplicate tables
- Migrations must import models the same way as application code

### Testing
- `tests/conftest.py` provides fixtures including database session setup
- Tests create tables automatically via Base.metadata.create_all()
- Use `get_db()` dependency override for route testing

### CI/CD
- **test-coverage.yml**: Runs on PR/main push, generates HTML coverage artifacts
- **deploy.yml**: Deploys to Render on main branch push, triggers scraping after deploy
- Both workflows use `uv` for dependency management

## Common Endpoints

- `GET /health/` - API health check and DB connectivity
- `GET /books/` - List books with pagination (query: page, per_page)
- `GET /books/{id}` - Get single book by ID
- `GET /books/search` - Search by title/category
- `GET /categories/` - List all categories with counts
- `POST /scraping/trigger` - Run web scraping process
- `GET /scraping/status` - Database statistics

All list endpoints return paginated responses with `next`/`previous` URLs.

## Data Model

**books** table:
- id (Integer, PK)
- title (String, unique, not null)
- price (Numeric(8,2), not null)
- rating (Integer, not null) - 1-5 scale
- availability (Boolean, default True)
- category (String, not null)
- image (String, nullable)
