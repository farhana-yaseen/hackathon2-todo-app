---
id: 001
title: Phase II constitution addition
stage: constitution
date: 2025-12-29
surface: agent
model: claude-sonnet-4.5-20250929
feature: none
branch: 001-todo-cli
user: zuni
command: /sp.constitution
labels: ["constitution", "phase-ii", "full-stack"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - N/A
---

## Prompt

The Phase I constitution will remain in effect, and this Phase II constitution will be added alongside it.
You are an expert Full-Stack System Architect. You utilize Spec-Driven Development via Claude Code and Spec-Kit Plus. Your mandate is to evolve the Phase I logic into a distributed system without writing manual boilerplate, instead refining specifications until the AI generates the correct implementation.

Project Vision
Phase II: Full-Stack Web Application
Transitioning from in-memory storage to a persistent, multi-user environment. This involves a decoupled architecture with a professional frontend, a robust REST API, and serverless database integration.

Technology Stack (Strict Adherence)
• Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS.
• Backend: Python, FastAPI.
• ORM: SQLModel (for Pydantic/SQL integration).
• Database: Neon Serverless PostgreSQL.
• Authentication: Better Auth (Frontend) + JWT Token Verification (Backend).
• Package Management: uv (Python), npm or pnpm (Node.js).

API Endpoints
GET /api/{user_id}/tasks List all tasks
POST /api/{user_id}/tasks Create new task
GET /api/{user_id}/tasks/{id} Get task details
PUT /api/{user_id}/tasks/{id} Update a task
DELETE /api/{user_id}/tasks/{id} Delete a task
PATCH /api/{user_id}/tasks/{id}/complete Toggle completion

Monorepo Structure
The project must follow the structured monorepo pattern to allow Claude Code to manage both stacks simultaneously:
codeText
hackathon-todo/
├── .spec-kit/ # Spec-Kit configuration
│ └── config.yaml
├── specs/ # Spec-Kit managed specifications
│ ├── overview.md # Project overview
│ ├── architecture.md # System architecture
│ ├── features/ # Feature specifications
│ │ ├── task-crud.md
│ │ ├── authentication.md
│ │ └── chatbot.md
│ ├── api/ # API specifications
│ │ ├── rest-endpoints.md
│ │ └── mcp-tools.md
│ ├── database/ # Database specifications
│ │ └── schema.md
│ └── ui/ # UI specifications
│ ├── components.md
│ └── pages.md
├── CLAUDE.md # Root Claude Code instructions
├── frontend/
│ ├── CLAUDE.md
│ └── ... (Next.js app)
├── backend/
│ ├── CLAUDE.md
│ └── ... (FastAPI app)
├── docker-compose.yml
└── README.md

Core Requirements (Basic Level + Persistence)
1. Multi-User Support: Tasks must be associated with a user_id.
2. RESTful API: Implement GET, POST, PUT, DELETE, and PATCH (for completion).
3. Authentication: Secure all API endpoints using JWT tokens.

Authentication Flow
• Frontend must include JWT in Authorization: Bearer <token> header for all API calls.
• Backend Validation: FastAPI must intercept requests, verify JWT, and extract user_id to filter database queries.

The Solution: JWT Tokens
Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.

How It Works
• User logs in on Frontend → Better Auth creates a session and issues a JWT token
• Frontend makes API call → Includes JWT token in Authorization: Bearer header
• Backend receives request → Extracts token from header, verifies signature using shared secret
• Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL
• Backend filters data → Returns only tasks belonging to that user

What Needs to Change
Component Changes Required
Better Auth Config Enable JWT plugin to issue tokens
Frontend API Client Attach JWT token to every API request header
FastAPI Backend Add middleware to verify JWT and extract user
API Routes Filter all queries by the authenticated user's ID

The Shared Secret
Both frontend (Better Auth) and backend (FastAPI) must use the same secret key for JWT signing and verification. This is typically set via environment variable BETTER_AUTH_SECRET in both services.

Security Benefits
Benefit Description
User Isolation Each user only sees their own tasks
Stateless Auth Backend doesn't need to call frontend to verify users
Token Expiry JWTs expire automatically (e.g., after 7 days)
No Shared DB Session Frontend and backend can verify auth independently

Authentication Rules
• All endpoints require valid JWT token
• Requests without token receive 401
• Unauthorized Each user only sees/modifies their own tasks
• Task ownership is enforced on every operation

Bottom Line
The REST API endpoints stay the same (GET /api/user_id/tasks, POST /api/user_id/tasks, etc.), but every request now must include a JWT token, and all responses are filtered to only include that user's data.

Coding Standards
• Clean Code: Follow PEP 8 (Python) and ESLint/Prettier (TS).
• Type Safety: 100% type hinting in Python; strict mode in TypeScript.
• API Conventions: Return JSON responses. Use Pydantic models for request/response validation.
• No Manual Code: All code changes must be initiated by updating a spec file or providing a prompt to Claude Code.

Execution Workflow
1. Spec First: Write @specs/database/schema.md and @specs/api/rest-endpoints.md.
2. Infrastructure: Initialize Neon DB and link it to the FastAPI backend.
3. Logic: Implement the Backend CRUD logic and test with Swagger UI (/docs).
4. Frontend: Build the Next.js UI and integrate Better Auth.
5. Integration: Connect the UI to the API via a centralized fetch client.

Python Version: 3.13+

## Response snapshot

Successfully updated constitution to version 2.0.0. Added Phase II full-stack web application principles alongside existing Phase I CLI principles.

Key additions:
- Phase II Core Principles (VII-XII): Monorepo Structure, API-First Design, Stateless Authentication, Security & Authorization, Spec-Driven Development, Multi-User Persistence
- Phase II Technology Stack: Next.js 16+, TypeScript, Tailwind CSS, FastAPI, SQLModel, Neon PostgreSQL, Better Auth
- Phase II API Endpoints: RESTful CRUD with JWT authentication
- Phase II Development Workflow: Spec-driven, quality gates for both Python and TypeScript
- Updated governance with cross-phase conflict resolution

Phase I (CLI) principles remain intact and apply to CLI code. Phase II (Full-Stack) principles apply to full-stack development. Templates verified for compatibility.

## Outcome

- ✅ Impact: Constitution extended from v1.0.0 to v2.0.0 with Phase II full-stack architecture principles
- 🧪 Tests: N/A (constitution update)
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Consider running /sp.spec or /sp.plan to begin Phase II implementation
- 🧠 Reflection: Constitution now supports dual-phase development - CLI code follows Phase I principles, full-stack code follows Phase II principles with clear separation of concerns.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider creating initial Phase II specifications (database schema, REST API endpoints) or ADR for monorepo structure decision
