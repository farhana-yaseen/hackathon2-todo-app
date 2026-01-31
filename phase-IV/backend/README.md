---
title: chatbot
sdk: docker
emoji: 🚀
colorFrom: purple
colorTo: pink
---
# Todo Backend

FastAPI backend for Phase II Full-Stack Todo Application.

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your DATABASE_URL and BETTER_AUTH_SECRET
   ```

3. **Run the server:**
   ```bash
   uv run uvicorn src.api.main:app --reload
   ```

4. **Open API docs:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | JWT secret for authentication |

## Project Structure

```
backend/
├── src/
│   ├── api/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── dependencies.py # DB and auth dependencies
│   │   └── routes/
│   │       └── tasks.py    # Task CRUD endpoints
│   ├── models/
│   │   └── task.py         # Task SQLModel
│   └── tests/
├── pyproject.toml
└── .env.example
```