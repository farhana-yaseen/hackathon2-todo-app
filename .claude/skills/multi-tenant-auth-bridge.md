name: "multi-tenant-auth-bridge"
description: "Implements secure, cross-language authentication. Bridges Better Auth (JS) with FastAPI (Python) using shared HS256 JWT secrets. Ensures User A cannot see User B's tasks."
version: "1.0.0"
---
# How This Skill Works
1. Configures Better Auth on Next.js to issue JWTs.
2. Creates a Python security utility using `PyJWT` or `python-jose`.
3. Implements a FastAPI `Depends(get_current_user)` function.
4. Refactors SQLModel queries to include `.where(Task.user_id == current_user.id)`.
5. Sets up CORS and middleware for secure header transmission.

# Critical Constraints
- Algorithm: HS256
- Shared Secret: BETTER_AUTH_SECRET (Env variable)
- Error Handling: 401 Unauthorized for expired/missing tokens.