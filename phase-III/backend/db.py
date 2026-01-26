"""Database and authentication dependencies for FastAPI backend.

This module provides:
- Database engine and session management
- JWT token verification
- User authentication dependencies
"""
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, status
from jwt import decode, encode, PyJWTError
from pydantic import BaseModel
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import NullPool

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "default-secret-change-in-production")

# Engine instance
_engine = None


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL not set")
        _engine = create_engine(
            db_url,
            echo=False,
            poolclass=NullPool,
            connect_args={"sslmode": "require"}
        )
    return _engine


def create_db_engine(echo: bool = False):
    """Create SQLModel database engine for Neon PostgreSQL."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set")
    return create_engine(
        db_url,
        echo=echo,
        poolclass=NullPool,
        connect_args={"sslmode": "require"}
    )


async def get_session() -> AsyncGenerator[Session, None]:
    """Dependency that provides a database session.

    Usage:
        @app.get("/tasks")
        async def list_tasks(session: Session = Depends(get_session)):
            return session.exec(select(Task)).all()
    """
    engine = get_engine()
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class TokenPayload(BaseModel):
    """JWT token payload model."""
    sub: str  # User ID
    exp: Optional[int] = None  # Expiration timestamp
    iat: Optional[int] = None  # Issued at timestamp


class AuthenticatedUser(BaseModel):
    """Authenticated user extracted from JWT token."""
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None


async def get_current_user(request: Request) -> AuthenticatedUser:
    """Dependency that extracts and validates JWT token from request.

    Checks in order:
    1. Authorization header: Bearer <token>
    2. auth_token cookie

    Args:
        request: FastAPI request object

    Returns:
        AuthenticatedUser with user_id and other claims

    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    authorization: Optional[str] = request.headers.get("Authorization")
    token = None

    # Try to get token from Authorization header first
    if authorization and authorization.startswith("Bearer"):
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]

    # If no token in header, try to get from cookies
    if not token:
        token = request.cookies.get("auth_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header or auth_token cookie",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode JWT token using the shared secret
        payload = decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "require": ["sub"],
            }
        )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user identifier",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return AuthenticatedUser(
            user_id=user_id,
            email=payload.get("email"),
            name=payload.get("name"),
        )

    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_auth(
    user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    """Dependency that requires authentication.

    Usage:
        @app.get("/tasks")
        async def list_tasks(user: AuthenticatedUser = Depends(require_auth)):
            # user.user_id is guaranteed to be valid
            ...
    """
    return user


class OwnershipError(HTTPException):
    """Custom exception for ownership violations."""

    def __init__(self, detail: str = "You do not have permission to access this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


async def verify_task_ownership(
    task_id: int,
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session),
) -> dict:
    """Dependency that verifies user owns the task.

    Args:
        task_id: ID of the task to check
        user: Authenticated user from JWT
        session: Database session

    Returns:
        Task data dict if ownership verified

    Raises:
        OwnershipError: 403 if user doesn't own the task
        HTTPException: 404 if task not found
    """
    from models import Task

    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.user_id != user.user_id:
        raise OwnershipError(
            detail=f"Task {task_id} does not belong to user {user.user_id}"
        )

    return task.model_dump()
