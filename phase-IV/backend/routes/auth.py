"""Authentication routes for the Todo API.

This module implements JWT-based authentication:
- Sign up: Creates a new user and returns a JWT token
- Sign in: Validates credentials and returns a JWT token
- Sign out: Clears the session cookie
- Session: Returns the current session info
"""
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Response, status, Depends
from jwt import decode, encode
from pydantic import BaseModel, EmailStr
from sqlmodel import Session as SQLModelSession, select
import bcrypt

from models import User
from db import get_session, get_current_user, AuthenticatedUser

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "default-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

import logging
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from authlib.integrations.starlette_client import OAuth

logger = logging.getLogger(__name__)

# OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

oauth = OAuth()

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

if GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET:
    oauth.register(
        name='github',
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'}
    )

# SMTP Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER)

# Password hashing functions using bcrypt directly
def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    # Truncate to 72 bytes for bcrypt compatibility
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash."""
    # Truncate to 72 bytes for bcrypt compatibility
    password_bytes = password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def send_verification_email(email: str, token: str):
    """Send a real verification email via SMTP."""
    frontend_url = os.getenv("FRONTEND_URL", "https://hackathon2-todo-app-three.vercel.app")
    verification_link = f"{frontend_url.replace('https://', '')}/auth/verify?token={token}"

    # Check if SMTP is configured
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning("SMTP not configured. Falling back to log-only verification.")
        logger.info(f"--- MOCK EMAIL ---")
        logger.info(f"To: {email}")
        logger.info(f"Link: {verification_link}")
        print(f"\n[EMAIL] Verify link for {email}: {verification_link}\n")
        return

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = MAIL_FROM
        msg['To'] = email
        msg['Subject'] = "Verify your Todo App account"

        body = f"""
        Hello,

        Thank you for registering for the Todo App!
        Please click the link below to verify your email address and activate your account:

        {verification_link}

        If you did not create an account, please ignore this email.

        Best regards,
        Todo App Team
        """
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Verification email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        # Log the link anyway so dev can continue if delivery fails
        logger.info(f"Verification link (recovery): {verification_link}")
        print(f"\n[ERROR] Could not send email. Verify link: {verification_link}\n")


def send_reset_password_email(email: str, token: str):
    """Send a password reset email via SMTP."""
    frontend_url = os.getenv("FRONTEND_URL", "https://hackathon2-todo-app-three.vercel.app")
    reset_link = f"{frontend_url}/auth/reset-password?token={token}"

    # Check if SMTP is configured
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.info(f"--- MOCK RESET EMAIL ---")
        logger.info(f"To: {email}")
        logger.info(f"Link: {reset_link}")
        print(f"\n[RESET EMAIL] Reset link for {email}: {reset_link}\n")
        return

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = MAIL_FROM
        msg['To'] = email
        msg['Subject'] = "Reset your Todo App password"

        body = f"""
        Hello,

        You requested to reset your password for the Todo App.
        Please click the link below to set a new password:

        {reset_link}

        This link will expire in 1 hour.

        If you did not request a password reset, please ignore this email.

        Best regards,
        Todo App Team
        """
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Password reset email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send reset email to {email}: {e}")
        logger.info(f"Reset link (recovery): {reset_link}")
        print(f"\n[ERROR] Could not send reset email. Reset link: {reset_link}\n")




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
    session: SQLModelSession = Depends(get_session)
):
    """Create a new user account and send verification email."""
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

    # Generate verification token
    v_token = secrets.token_urlsafe(32)

    # Create user
    user = User(
        email=request.email,
        name=request.name,
        password_hash=password_hash,
        is_verified=False,
        verification_token=v_token
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Send verification email
    send_verification_email(user.email, v_token)

    # Create JWT token (even if not verified, for some flows,
    # but normally we might wait for verification)
    token = create_access_token(user.id, user.email, user.name)

    # Set cookie with consistent cross-domain settings
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,  # Always use secure in production environments
        samesite="none",  # Required for cross-origin requests
        max_age=60 * 60 * 24 * 7,
    )
    return SignUpResponse(
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
        token=token
    )


@router.get("/verify-email")
async def verify_email(token: str, session: SQLModelSession = Depends(get_session)):
    """Verify user's email with token."""
    statement = select(User).where(User.verification_token == token)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )

    if user.is_verified:
        return {"message": "Email already verified"}

    user.is_verified = True
    user.verification_token = None
    session.add(user)
    session.commit()

    return {"message": "Email verified successfully. You can now log in."}


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(
    request: SignInRequest,
    response: Response,
    session: SQLModelSession = Depends(get_session)
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

    # Check if verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in",
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

    # Set cookie with consistent cross-domain settings
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,  # Always use secure in production environments
        samesite="none",  # Required for cross-origin requests
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
        secure=True,  # Always use secure in production environments
        samesite="none",  # Required for cross-origin requests
    )
    return {"message": "Signed out successfully"}


@router.get("/login/{provider}")
async def login_via_provider(provider: str, request: Request):
    """Initiate OAuth login flow."""
    # Try to construct the backend URL based on the current request in proxy environments
    if request.url.hostname and "huggingface" in request.url.hostname:
        # Special handling for Hugging Face Spaces
        scheme = "https"
        hostname = request.url.hostname
        port = ""
        if request.url.port and request.url.port != 443:
            port = f":{request.url.port}"
        BACKEND_URL = f"{scheme}://{hostname}{port}"
    else:
        # Use environment variable or default
        BACKEND_URL = os.getenv(
            "BACKEND_URL",
            f"{request.url.scheme}://{request.url.netloc}"
        )

        # Ensure the redirect_uri uses HTTPS, especially important for reverse proxy setups like Hugging Face Spaces
        if BACKEND_URL.startswith("http://"):
            BACKEND_URL = "https://" + BACKEND_URL[7:]  # Replace http:// with https://
        elif not BACKEND_URL.startswith("https://"):
            BACKEND_URL = "https://" + BACKEND_URL  # Add https:// if neither is present

    redirect_uri = f"{BACKEND_URL}/api/auth/callback/{provider}"
    print(f"OAuth redirect_uri for {provider}: {redirect_uri}")  # Debug logging

    # Note: Use a frontend callback URL if you want a cleaner separation,
    # but here we redirect directly through the backend callback.
    if provider == "google":
        return await oauth.google.authorize_redirect(request, str(redirect_uri))
    elif provider == "github":
        return await oauth.github.authorize_redirect(request, str(redirect_uri))
    else:
        raise HTTPException(status_code=400, detail="Invalid provider")


@router.get("/callback/{provider}", name="auth_callback")
async def auth_callback(
    provider: str,
    request: Request,
    response: Response,
    db_session: SQLModelSession = Depends(get_session)
):
    """Handle OAuth callback and create/login user."""
    try:
        if provider == "google":
            token = await oauth.google.authorize_access_token(request)
            user_info = token.get('userinfo')
        elif provider == "github":
            token = await oauth.github.authorize_access_token(request)
            user_resp = await oauth.github.get('user', token=token)
            user_info = user_resp.json()
            # GitHub email might need a separate call
            if not user_info.get('email'):
                emails_resp = await oauth.github.get('user/emails', token=token)
                emails = emails_resp.json()
                primary_email = next((e['email'] for e in emails if e['primary']), emails[0]['email'])
                user_info['email'] = primary_email
        else:
            raise HTTPException(status_code=400, detail="Invalid provider")

        email = user_info.get('email')
        name = user_info.get('name') or user_info.get('login') or email.split('@')[0]

        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by OAuth provider")

        # Check if user exists
        statement = select(User).where(User.email == email)
        user = db_session.exec(statement).first()

        if not user:
            # Create user if doesn't exist
            # Note: We generate a random password hash they can't use directly
            user = User(
                email=email,
                name=name,
                password_hash=hash_password(secrets.token_urlsafe(32)),
                is_verified=True # Social logins are pre-verified
            )
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)

        # Create JWT token
        token_str = create_access_token(user.id, user.email, user.name)

        # Redirect to frontend - use your Vercel URL
        frontend_url = os.getenv("FRONTEND_URL", "https://hackathon2-todo-app-three.vercel.app")
        # Redirect without token in URL - frontend will call /api/auth/session to get the token
        from fastapi.responses import RedirectResponse
        redirect_response = RedirectResponse(url=f"{frontend_url}/auth/callback/{provider}")

        # Set the auth cookie on the redirect response with consistent cross-domain settings
        redirect_response.set_cookie(
            key="auth_token",
            value=token_str,
            httponly=True,
            secure=True,  # Always use secure in production environments
            samesite="none",  # Required for cross-origin requests
            max_age=60 * 60 * 24 * 7,
        )

        return redirect_response

    except Exception as e:
        logger.error(f"OAuth error: {str(e)}")
        frontend_url = os.getenv("FRONTEND_URL", "https://hackathon2-todo-app-three.vercel.app")
        from fastapi.responses import RedirectResponse
        redirect_response = RedirectResponse(url=f"{frontend_url}/auth/sign-in?error=OAuth failed")

        return redirect_response


@router.get("/session", response_model=SessionResponse)
async def get_session(request: Request):
    """Get the current session info."""
    authorization: Optional[str] = request.headers.get("Authorization")

    token = None

    # Try to get token from Authorization header first
    if authorization and authorization.startswith("Bearer"):
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


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db_session: SQLModelSession = Depends(get_session)
):
    """Generate reset token and send email."""
    statement = select(User).where(User.email == request.email)
    user = db_session.exec(statement).first()

    if not user:
        # Don't reveal account existence for security
        return {"message": "If an account exists with that email, a reset link has been sent."}

    # Generate token
    token = secrets.token_urlsafe(32)
    user.reset_password_token = token
    user.reset_password_expires_at = datetime.utcnow() + timedelta(hours=1)

    db_session.add(user)
    db_session.commit()

    # Send email
    send_reset_password_email(user.email, token)

    return {"message": "If an account exists with that email, a reset link has been sent."}


@router.post("/resend-verification")
async def resend_verification(
    request: ResendVerificationRequest,
    db_session: SQLModelSession = Depends(get_session)
):
    """Resend verification email to user."""
    statement = select(User).where(User.email == request.email)
    user = db_session.exec(statement).first()

    if not user:
        # Avoid user enumeration
        return {"message": "If this email is registered, a new verification link has been sent."}

    if user.is_verified:
        return {"message": "Email is already verified."}

    # Generate new token if needed or reuse existing
    if not user.verification_token:
        user.verification_token = secrets.token_urlsafe(32)
        db_session.add(user)
        db_session.commit()

    send_verification_email(user.email, user.verification_token)

    return {"message": "Verification email sent. Please check your inbox."}


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db_session: SQLModelSession = Depends(get_session)
):
    """Verify reset token and update password."""
    statement = select(User).where(
        User.reset_password_token == request.token,
        User.reset_password_expires_at > datetime.utcnow()
    )
    user = db_session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    # Update password
    user.password_hash = hash_password(request.new_password)
    user.reset_password_token = None
    user.reset_password_expires_at = None

    db_session.add(user)
    db_session.commit()

    return {"message": "Password reset successfully. You can now log in."}


@router.get("/profile")
async def get_profile(request: Request):
    """Get current user profile."""
    user_data = await get_current_user(request)

    # Get database session
    from db import get_engine
    from sqlmodel import Session as DBSession
    engine = get_engine()
    with DBSession(engine) as session:
        # Get full user details from database
        statement = select(User).where(User.id == user_data.user_id)
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat(),
        }


@router.put("/profile")
async def update_profile(
    request: Request,
    update_data: UpdateProfileRequest
):
    """Update user profile."""
    user_data = await get_current_user(request)

    # Get database session
    from db import get_engine
    from sqlmodel import Session as DBSession
    engine = get_engine()
    with DBSession(engine) as session:
        # Get user from database
        statement = select(User).where(User.id == user_data.user_id)
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Update fields if provided
        if update_data.name is not None:
            user.name = update_data.name

        if update_data.email is not None:
            # Check if email already exists
            existing = session.exec(
                select(User).where(User.email == update_data.email, User.id != user.id)
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use",
                )
            user.email = update_data.email

        session.add(user)
        session.commit()
        session.refresh(user)

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "message": "Profile updated successfully",
        }


@router.post("/change-password")
async def change_password(
    request: Request,
    password_data: ChangePasswordRequest
):
    """Change user password."""
    user_data = await get_current_user(request)

    # Get database session
    from db import get_engine
    from sqlmodel import Session as DBSession
    engine = get_engine()
    with DBSession(engine) as session:
        # Get user from database
        statement = select(User).where(User.id == user_data.user_id)
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Verify current password
        if not verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        # Update password
        user.password_hash = hash_password(password_data.new_password)
        session.add(user)
        session.commit()

        return {"message": "Password changed successfully"}
