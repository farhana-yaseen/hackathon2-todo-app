---
id: 1
title: Fix Auth Errors in FastAPI Vercel HuggingFace Integration
stage: refactor
date_iso: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: fix-authentication-issues
labels: ["auth", "security", "cookies", "oauth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - D:\hackthon\hackathon2\phase-III\backend\routes\auth.py
  - D:\hackthon\hackathon2\phase-III\backend\main.py
  - D:\hackthon\hackathon2\phase-III\frontend\app\auth\callback\[provider]\page.tsx
tests_yaml:
  - "Manual testing of auth flow"
---

# Fix Auth Errors in FastAPI Vercel HuggingFace Integration

## Problem Statement

Fixed authentication errors in the FastAPI application deployed on Vercel with Hugging Face backend:

1. **Cookies Not Sent in Cross-Domain Requests**: Auth cookies were set with SameSite="lax" and Secure=False, causing browsers to block them when frontend (vercel.app) and backend (hf.space) are on different domains.

2. **Mixed Authentication Systems**: The app used both SessionMiddleware and JWT tokens in cookies, causing inconsistent authentication behavior.

3. **OAuth Token Passed in URL**: OAuth callback sent JWT in query params, causing token leaks and auth desync.

## Solution Implemented

### 1. Fixed Cookie Configuration
- Updated all cookie settings to use consistent cross-domain values:
  - `httponly=True`
  - `secure=True` (always in production)
  - `samesite="none"` (required for cross-origin requests)

### 2. Removed SessionMiddleware
- Removed SessionMiddleware from `main.py` since the app uses JWT-based authentication
- Removed the import of SessionMiddleware
- Kept only JWT authentication system for consistency

### 3. Fixed OAuth Security Issue
- Modified OAuth callback in backend to not pass token in URL query parameter
- Updated frontend callback page to call `/api/auth/session` endpoint after redirect to get token securely
- Removed token from URL parameters to prevent token leakage

## Files Changed

- `backend/routes/auth.py`: Updated cookie settings for all auth endpoints and OAuth callback
- `backend/main.py`: Removed SessionMiddleware configuration and import
- `frontend/app/auth/callback/[provider]/page.tsx`: Updated to fetch session token securely after redirect

## Testing

Manually tested the authentication flow to ensure:
- Login and signup work correctly
- OAuth login works without token in URL
- Session persistence works properly
- Cross-domain requests are handled correctly

## Outcome

The authentication system now properly handles cross-domain requests between Vercel frontend and Hugging Face backend, eliminates mixed authentication systems, and prevents OAuth token leakage through URL parameters.

## Response Text

Fixed all three authentication issues:
1. Standardized cookie settings to use secure, httponly, and samesite="none" consistently
2. Removed SessionMiddleware to eliminate mixed auth systems
3. Updated OAuth flow to securely retrieve token via session endpoint instead of URL parameters