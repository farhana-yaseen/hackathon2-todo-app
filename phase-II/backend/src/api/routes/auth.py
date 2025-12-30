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
import hashlib
from datetime import datetime, timedelta
from typing import Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter, HTTPException, Request, Response, status
from jwt import decode, encode
from pydantic import BaseModel, EmailStr

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "default-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Use hashlib for password hashing (simple for demo - use bcrypt in production)
def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt."""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}:{hash_obj.hexdigest()}"

def verify_password(password: str, stored: str) -> bool:
    """Verify password against stored hash."""
    try:
        salt, hash_val = stored.split(":")
        hash_obj = hashlib.sha256((password + salt).encode())
        return hash_obj.hexdigest() == hash_val
    except (ValueError, TypeError):
        return False

# In-memory user store for demo (replace with real database in production)
# Format: {email: {"id": user_id, "email": email, "name": name, "password_hash": hash}}
_users_db: dict[str, dict] = {}


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
async def sign_up(request: SignUpRequest, response: Response):
    """Create a new user account and return a JWT token."""
    # Check if user already exists
    if request.email in _users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash password
    password_hash = hash_password(request.password)

    # Create user
    user_id = generate_user_id()
    user = {
        "id": user_id,
        "email": request.email,
        "name": request.name,
    }
    _users_db[request.email] = {
        **user,
        "password_hash": password_hash,
    }

    # Create JWT token
    token = create_access_token(user_id, request.email, request.name)

    # Set cookie
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,  # Set to False for localhost development
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return SignUpResponse(user=user, token=token)


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(request: SignInRequest, response: Response):
    """Authenticate user and return a JWT token."""
    # Check if user exists
    user_data = _users_db.get(request.email)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(request.password, user_data["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token
    token = create_access_token(
        user_data["id"],
        user_data["email"],
        user_data["name"],
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
            "id": user_data["id"],
            "email": user_data["email"],
            "name": user_data["name"],
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
