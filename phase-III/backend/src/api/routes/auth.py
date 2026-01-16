"""Authentication routes for the Todo API.

This module implements JWT-based authentication:
- Sign up: Creates a new user and returns a JWT token
- Sign in: Validates credentials and returns a JWT token
- Sign out: Clears the session cookie
- Session: Returns the current session info
"""
import os
import sys
import secrets
from datetime import datetime, timedelta
from typing import Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter, HTTPException, Request, Response, status, Depends
from jwt import decode, encode
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from passlib.context import CryptContext

from models.task import User
from api.dependencies import get_session

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "default-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash."""
    return pwd_context.verify(password, hashed_password)


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpResponse(BaseModel):
    user: dict
    token: str


class SignInResponse(BaseModel):
    user: dict
    token: str


class SessionResponse(BaseModel):
    user: dict
    token: str


router = APIRouter(prefix="/api/auth", tags=["auth"])


def create_access_token(user_id: str, email: str, name: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token for the user."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": user_id,
        "email": email,
        "name": name,
        "iat": datetime.utcnow(),
        "exp": expire,
    }
    return encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)


def generate_user_id() -> str:
    """Generate a unique user ID."""
    return secrets.token_urlsafe(16)


@router.post("/sign-up", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
    request: SignUpRequest,
    response: Response,
    session: Session = Depends(get_session)
):
    """Create a new user account and return a JWT token."""
    # Check if user already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash password
    password_hash = hash_password(request.password)

    # Create user
    user = User(
        email=request.email,
        name=request.name,
        password_hash=password_hash,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create JWT token
    token = create_access_token(user.id, user.email, user.name)

    # Set cookie
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,  # Set to False for localhost development
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return SignUpResponse(
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
        token=token
    )


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(
    request: SignInRequest,
    response: Response,
    session: Session = Depends(get_session)
):
    """Authenticate user and return a JWT token."""
    # Check if user exists
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token
    token = create_access_token(
        user.id,
        user.email,
        user.name,
    )

    # Set cookie
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return SignInResponse(
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
        token=token,
    )


@router.post("/sign-out")
async def sign_out(response: Response):
    """Clear the session cookie."""
    response.delete_cookie(
        key="auth_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"message": "Signed out successfully"}


@router.get("/session", response_model=SessionResponse)
async def get_session(request: Request):
    """Get the current session info."""
    authorization: Optional[str] = request.headers.get("Authorization")

    token = None

    # Try to get token from Authorization header first
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
    else:
        # Try to get token from cookies
        token = request.cookies.get("auth_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM],
            options={"verify_signature": True, "verify_exp": True},
        )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        return SessionResponse(
            user={
                "id": user_id,
                "email": payload.get("email", ""),
                "name": payload.get("name", ""),
            },
            token=token,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        )
