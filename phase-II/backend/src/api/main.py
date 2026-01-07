"""FastAPI application main point.

Phase II Full-Stack Todo Application - Backend
"""
import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan events."""
    # Startup
    logger.info("Starting Todo Backend API...")
    logger.info("Database connection will be established on first request")
    yield
    # Shutdown
    logger.info("Shutting down Todo Backend API...")


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="RESTful API for Phase II Full-Stack Todo Application",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for frontend
origins = [
    "http://localhost:3000",  # Next.js default port
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__,
        },
    )


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "healthy", "service": "todo-backend"}


# Import and include routers
from src.api.routes.tasks import router as tasks_router
from src.api.routes.notifications import router as notifications_router
from src.api.routes import auth
from src.api.dependencies import get_engine
from sqlmodel import SQLModel

app.include_router(tasks_router)
app.include_router(auth.router)
app.include_router(notifications_router)

# Initialize database tables at module load time (dev mode: drop and recreate)
engine = get_engine()
# SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)
logger.info("Database tables initialized (dropped and recreated)")


# Root endpoint
@app.get("/", tags=["root"])
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "service": "Todo Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
