# Implementation Plan: Phase II Full-Stack Web Application

**Branch**: `002-full-stack-web` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-full-stack-web/spec.md`

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for execution workflow.

## Summary

Transition from in-memory CLI todo application to persistent, multi-user full-stack web application using decoupled monorepo architecture with Next.js frontend, FastAPI backend, and Neon PostgreSQL database with JWT-based authentication.

## Technical Context

**Language/Version**: Python 3.13+, TypeScript (strict)
**Primary Dependencies**: FastAPI, SQLModel, Next.js 16+, Tailwind CSS, Better Auth, PyJWT
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Jest/Vitest (frontend optional)
**Target Platform**: Web browser, server deployment
**Project Type**: web (frontend + backend)
**Performance Goals**: API responses <200ms p95, page load <3s, 100 concurrent users
**Constraints**: JWT verification on all endpoints, user data isolation enforced at DB level, <1000 tasks per user manageable
**Scale/Scope**: Multi-user SaaS application, REST API, Next.js App Router

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase II Principles Compliance

- [x] **VII. Monorepo Structure** - Frontend/backend separation in independent deployable services
- [x] **VIII. API-First Design** - RESTful contracts with OpenAPI docs
- [x] **IX. Stateless Authentication** - JWT tokens with Better Auth issuance, shared secret validation
- [x] **X. Security & Authorization** - 401 on missing token, user ownership enforcement, middleware verification
- [x] **XI. Spec-Driven Development** - Spec first, no manual boilerplate, contract tests
- [x] **XII. Multi-User Persistence** - User association, Neon DB, SQLModel ORM, migrations

### Code Quality Gates (Phase II)

- [x] **Type Safety**: 100% type hinting (Python), strict TypeScript mode
- [x] **Clean Code**: PEP 8 (Python), ESLint/Prettier (TypeScript)
- [x] **Pydantic Models**: All request/response schemas validated
- [x] **JWT Verification**: All endpoints have auth middleware
- [x] **User Isolation**: All queries filtered by user_id

**GATE PASSED**: All Phase II principles satisfied. Proceed to implementation planning.

## Project Structure

### Documentation (this feature)

```text
specs/002-full-stack-web/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application (frontend + backend)
backend/
├── src/
│   ├── models/
│   │   └── task.py          # Task SQLModel
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py      # DB session, auth dependencies
│   │   ├── routes/
│   │   │   ├── tasks.py      # Task CRUD endpoints
│   │   │   └── auth.py       # Auth utilities
│   │   └── main.py            # FastAPI app setup
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_task_model.py
│   │   │   └── test_task_routes.py
│   │   └── integration/
│   │       └── test_api_e2e.py
│   ├── pyproject.toml
│   └── .env.example
└── README.md

frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx           # Landing/login page
│   │   ├── dashboard/
│   │   │   └── page.tsx      # Protected dashboard
│   │   ├── layout.tsx          # Root layout with navbar
│   │   ├── components/
│   │   │   ├── Navbar.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   ├── TaskList.tsx
│   │   │   └── TaskItem.tsx
│   │   ├── lib/
│   │   │   └── api.ts      # Fetch client with JWT
│   │   └── auth.tsx            # Better Auth config
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── README.md

.env.example                      # Shared secrets (BETTER_AUTH_SECRET, DATABASE_URL)
docker-compose.yml                 # Local development orchestration
README.md                        # Root documentation
CLAUDE.md                        # Root Claude Code instructions
```

**Structure Decision**: Structured monorepo with independent frontend (Next.js) and backend (FastAPI) services, communicating via REST API. Backend handles database access, frontend handles UI and auth, with shared environment configuration for secrets.

## Complexity Tracking

> No violations - all complexity justified by Phase II requirements

## Phase 0: Research & Architecture Decisions

### Research Tasks

- [ ] R001 Research Better Auth JWT configuration patterns
- [ ] R002 Research FastAPI JWT middleware best practices
- [ ] R003 Research SQLModel with Neon PostgreSQL connection patterns
- [ ] R004 Research Next.js App Router with protected routes
- [ ] R005 Research JWT library for Python (PyJWT vs jose)

**Checkpoint**: All research consolidated and architectural decisions documented in research.md

---

## Phase 1: Design & Contracts

### Data Model Design

**Goal**: Define database schema and API contracts

- [ ] D001 Create User model (SQLModel) in backend/src/models/user.py
- [ ] D002 Create Task model (SQLModel) in backend/src/models/task.py
- [ ] D003 Define relationships (Task.user_id → User.id)
- [ ] D004 Add validation rules (title length, description length)
- [ ] D005 Define indexes (user_id, created_at) for performance

**Checkpoint**: Data models ready, database schema documented in data-model.md

### API Contracts

**Goal**: Define REST API endpoints with request/response schemas

- [ ] C001 Define GET /api/tasks - ListTasksRequest, ListTasksResponse
- [ ] C002 Define POST /api/tasks - CreateTaskRequest, TaskResponse
- [ ] C003 Define GET /api/tasks/{id} - TaskResponse
- [ ] C004 Define PUT /api/tasks/{id} - UpdateTaskRequest, TaskResponse
- [ ] C005 Define PATCH /api/tasks/{id}/complete - TaskResponse
- [ ] C006 Define DELETE /api/tasks/{id} - SuccessResponse
- [ ] C007 Define error response schemas (401, 403, 404)
- [ ] C008 Generate OpenAPI/Swagger spec in contracts/rest-openapi.yaml

**Checkpoint**: All API contracts defined and documented in contracts/

### Quickstart Guide

**Goal**: Provide setup instructions for local development

- [ ] Q001 Document environment setup (.env configuration)
- [ ] Q002 Document backend startup (uvicorn with database)
- [ ] Q003 Document frontend dev server (npm run dev)
- [ ] Q004 Document testing endpoints (Swagger UI, frontend)

**Checkpoint**: Developers can run both services locally

---

## Phase 2: Foundation & Configuration

**Purpose**: Set up project structure and core infrastructure

### Backend Setup

- [ ] F001 Initialize backend with uv (create pyproject.toml)
- [ ] F002 Install dependencies: fastapi, uvicorn, sqlmodel, psycopg2-binary, pyjwt
- [ ] F003 Create backend/src/ directory structure
- [ ] F004 Configure .env.example with DATABASE_URL placeholder
- [ ] F005 Create backend/src/api/main.py FastAPI app
- [ ] F006 Configure CORS middleware for frontend origin
- [ ] F007 Setup logging configuration

### Frontend Setup

- [ ] F008 Initialize frontend with Next.js (create-next-app)
- [ ] F009 Install dependencies: better-auth, tailwindcss
- [ ] F010 Configure TypeScript strict mode
- [ ] F011 Setup Tailwind CSS
- [ ] F012 Create frontend/src/app directory structure
- [ ] F013 Configure Better Auth in auth.tsx

### Shared Configuration

- [ ] F014 Create root .env.example with BETTER_AUTH_SECRET, DATABASE_URL
- [ ] F015 Create docker-compose.yml for local development
- [ ] F016 Update root README.md with monorepo setup instructions

**Checkpoint**: Project structure ready, both stacks can be initialized

---

## Phase 3: Backend Implementation

**Purpose**: Implement FastAPI backend with database and authentication

### Database Layer

- [ ] B001 Create database engine configuration (SQLModel)
- [ ] B002 Implement session management (SQLModel Session)
- [ ] B003 Create migration script for User and Task tables
- [ ] B004 Add database connection error handling

### Authentication Layer

- [ ] A001 Create get_current_user dependency in backend/src/api/dependencies.py
- [ ] A002 Implement JWT decode function using PyJWT
- [ ] A003 Verify BETTER_AUTH_SECRET from environment
- [ ] A004 Create HTTPException for 401 Unauthorized
- [ ] A005 Create HTTPException for 403 Forbidden

### API Routes - Tasks

- [ ] T001 Implement GET /api/tasks - list tasks filtered by user_id
- [ ] T002 Implement POST /api/tasks - create task with user_id
- [ ] T003 Implement GET /api/tasks/{id} - get task with ownership check
- [ ] T004 Implement PUT /api/tasks/{id} - update task with ownership check
- [ ] T005 Implement PATCH /api/tasks/{id}/complete - toggle completion
- [ ] T006 Implement DELETE /api/tasks/{id} - delete with ownership check
- [ ] T007 Add Pydantic request/response models
- [ ] T008 Add OpenAPI documentation (automatic via FastAPI)

### Testing

- [ ] S001 Write unit tests for Task model
- [ ] S002 Write unit tests for authentication logic
- [ ] S003 Write integration tests for all task endpoints
- [ ] S004 Test 401 Unauthorized scenario
- [ ] S005 Test 403 Forbidden (cross-user access)
- [ ] S006 Test 404 Not Found

**Checkpoint**: Backend CRUD complete, tested, Swagger docs available at /docs

---

## Phase 4: Frontend Implementation

**Purpose**: Implement Next.js UI with Better Auth and API integration

### Authentication

- [ ] FA001 Configure Better Auth with email provider
- [ ] FA002 Implement login page (/)
- [ ] FA003 Implement logout functionality
- [ ] FA004 Store JWT token in session/localStorage

### API Client

- [ ] AP001 Create fetch wrapper in frontend/src/app/lib/api.ts
- [ ] AP002 Add JWT token to Authorization header on all requests
- [ ] AP003 Add TypeScript types for API requests/responses
- [ ] AP004 Implement error handling (401, 403, 404)

### UI Components

- [ ] U001 Create Navbar component with logout button
- [ ] U002 Create TaskForm component (modal/inline)
- [ ] U003 Create TaskList component
- [ ] U004 Create TaskItem component with status toggle and delete
- [ ] U005 Implement loading states
- [ ] U006 Implement error handling display

### Pages

- [ ] P001 Create landing/login page (/)
- [ ] P002 Create dashboard page (/dashboard) with protected route
- [ ] P003 Add middleware for JWT token verification on protected routes

**Checkpoint**: Frontend UI complete, connected to backend API

---

## Phase 5: Integration & Security

**Purpose**: Connect frontend and backend, verify security

### End-to-End Integration

- [ ] I001 Test login flow (Better Auth → JWT token → dashboard)
- [ ] I002 Test task creation (frontend → API → database → display)
- [ ] I003 Test user isolation (login User A, create task, logout, login User B)
- [ ] I004 Test JWT expiry (token expiration, redirect to login)
- [ ] I005 Test concurrent user sessions

### Security Verification

- [ ] V001 Verify 401 returned for requests without JWT
- [ ] V002 Verify 403 returned for cross-user access attempts
- [ ] V003 Verify user_id filtering in all database queries
- [ ] V004 Verify BETTER_AUTH_SECRET consistency (frontend/backend)
- [ ] V005 Verify no direct database access from frontend

### Performance Testing

- [ ] PE001 Test API response times (target <200ms p95)
- [ ] PE002 Test page load times (target <3s)
- [ ] PE003 Test with 100+ concurrent users
- [ ] PE004 Test database query performance (1000 tasks user)

**Checkpoint**: Full integration tested, security verified, performance meets criteria

---

## Phase 6: Polish & Deployment

**Purpose**: Finalize documentation and prepare for deployment

### Documentation

- [ ] D001 Update backend/README.md with setup instructions
- [ ] D002 Update frontend/README.md with setup instructions
- [ ] D003 Document environment variables in root README.md
- [ ] D004 Document deployment process

### Code Quality

- [ ] Q001 Run mypy on backend (0 errors)
- [ ] Q002 Run ruff on backend (0 warnings)
- [ ] Q003 Run TypeScript strict check on frontend
- [ ] Q004 Run ESLint on frontend (0 errors)
- [ ] Q005 Format all code (Prettier on frontend, ruff format on backend)

### Deployment Preparation

- [ ] DP001 Create production .env template
- [ ] DP002 Configure Neon database for production
- [ ] DP003 Setup production environment variables
- [ ] DP004 Prepare Docker configuration for deployment

**Checkpoint**: Ready for production deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Research (Phase 0)**: No dependencies - can start immediately
- **Design & Contracts (Phase 1)**: Depends on Research completion - BLOCKS implementation
- **Foundation & Configuration (Phase 2)**: Depends on Design & Contracts - BLOCKS Backend and Frontend
- **Backend Implementation (Phase 3)**: Depends on Foundation - INDEPENDENT from Frontend
- **Frontend Implementation (Phase 4)**: Depends on Foundation - INDEPENDENT from Backend
- **Integration & Security (Phase 5)**: Depends on Backend AND Frontend completion
- **Polish & Deployment (Phase 6)**: Depends on Integration completion

### Parallel Opportunities

- **Within Research (Phase 0)**: All research tasks can run in parallel
- **Within Design & Contracts (Phase 1)**: Data model and API contracts can run in parallel
- **Within Foundation & Configuration (Phase 2)**: Backend setup and Frontend setup can run in parallel
- **Within Backend Implementation (Phase 3)**: Routes can be implemented in parallel after models/auth done
- **Within Frontend Implementation (Phase 4)**: Components can be developed in parallel
- **Within Testing**: Unit tests and integration tests can run in parallel

---

## Implementation Strategy

### MVP First (Backend Priority)

1. Complete Phase 0: Research
2. Complete Phase 1: Design & Contracts
3. Complete Phase 2: Foundation & Configuration (backend first)
4. Complete Phase 3: Backend Implementation
5. **STOP and VALIDATE**: Test backend with Swagger UI (/docs) and curl/postman
6. Test authentication flow with mock frontend
7. Complete Phase 4: Frontend Implementation
8. Complete Phase 5: Integration & Security

### Incremental Delivery

1. Research + Design + Foundation → Architecture ready
2. Backend Implementation → Test with Swagger → Ready for frontend
3. Frontend Implementation → Test with mock API → Connect to real backend
4. Integration → Full E2E testing → Ready for production
5. Polish → Documentation → Deploy

### Parallel Team Strategy

With multiple developers:

1. Team completes Research + Design + Foundation together
2. Once Foundation is done:
   - Developer A: Backend Implementation (Phase 3)
   - Developer B: Frontend Implementation (Phase 4)
3. Both teams complete in parallel, then integrate (Phase 5)
4. Together complete polish and deployment (Phase 6)

---

## Notes

- Better Auth manages User table; backend only needs Task model with user_id foreign key
- JWT verification MUST happen on every API request
- All database queries MUST filter by user_id
- Frontend should never connect directly to database
- Use shared BETTER_AUTH_SECRET across both services
- Neon PostgreSQL provides serverless, auto-scaling database
- SQLModel integrates Pydantic (validation) and SQLAlchemy (ORM)
