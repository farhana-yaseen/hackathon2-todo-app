"""FastAPI application main point.

Phase II Full-Stack Todo Application - Backend
"""
import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse

# Import ProxyHeadersMiddleware with fallback for different Starlette versions
try:
    from starlette.middleware.proxy_headers import ProxyHeadersMiddleware
except ImportError:
    # If ProxyHeadersMiddleware is not available, define a minimal replacement
    from starlette.middleware.base import BaseHTTPMiddleware

    class ProxyHeadersMiddleware(BaseHTTPMiddleware):
        def __init__(self, app, trusted_hosts="*"):
            super().__init__(app)
            self.trusted_hosts = trusted_hosts

        async def dispatch(self, request, call_next):
            # Minimal implementation that just passes through the request
            response = await call_next(request)
            return response

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

# Configure CORS for frontend - Allow all origins in Kubernetes environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Kubernetes internal communication
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add ProxyHeadersMiddleware to handle reverse proxy headers (important for HTTPS detection behind Hugging Face Spaces)
# This ensures that X-Forwarded-* headers are properly trusted and used to determine the original request
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Add SessionMiddleware for OAuth with proper configuration for cross-domain requests
# NOTE: Required for OAuth state management by authlib, but JWT is still the primary auth method
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "default-session-secret-change-in-production"),
    session_cookie="session",
    max_age=60 * 60 * 24 * 7,  # 7 days
    same_site="none",  # Required for cross-domain OAuth flow
    https_only=True  # Always use secure in production
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
from routes.tasks import router as tasks_router
from routes.notifications import router as notifications_router
from routes import auth
from routes.chat import router as chat_router
from db import get_engine
from sqlmodel import SQLModel
from websocket_manager import manager, broadcast_task_update

app.include_router(tasks_router)
app.include_router(auth.router)
app.include_router(notifications_router)
app.include_router(chat_router)

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        # Keep the connection alive - we only send from server to client
        # The client doesn't need to send messages for real-time updates to work
        while True:
            # Wait for any data from client (this will raise WebSocketDisconnect if connection closes)
            data = await websocket.receive_text()
            # Optionally process any incoming messages if needed
            # For real-time updates, we mostly just send from server to client
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

# Initialize database tables at module load time
engine = get_engine()
# Only create tables if they don't exist (preserving data)
SQLModel.metadata.create_all(engine)
logger.info("Database tables initialized (preserved existing data)")


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
