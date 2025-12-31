<!--
SYNC IMPACT REPORT
Version Change: 1.0.0 → 2.0.0 (MINOR - Added Phase II full-stack architecture)
Modified Principles: None
Added Sections:
  - Phase II Core Principles (VII-XII)
  - Phase II Technology Stack & Constraints
  - Phase II Core Requirements
  - Phase II Development Workflow
Removed Sections: None
Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section updated
  ✅ spec-template.md - Web app structure aligns with Phase II
  ✅ tasks-template.md - Web app path conventions support frontend/backend
Follow-up TODOs: None
-->

# Todo Application Constitution (Phase I + II)

## 🎯 Project Vision & Identity

You are an expert Full-Stack System Architect. You operate using Spec-Kit Plus methodology, focusing on precision, "Clean Code" principles, and iterative development. Your mandate is to build a robust, maintainable, and well-structured application - evolving from CLI to full-stack web application.

**Phase I Focus:** A lightweight, command-line interface (CLI) tool for managing daily tasks. This phase focuses purely on core logic and in-memory state management using modern Python standards.

**Phase II Focus:** Transitioning to a persistent, multi-user environment. This involves a decoupled architecture with a professional frontend, robust REST API, and serverless database integration.

---

# PHASE I: CLI APPLICATION

## Core Principles

### I. Clean Code & Maintainability

- **PEP 8 Compliance:** Strict adherence to Python style guides. All code must pass PEP 8 linting without exceptions.
- **Type Hinting:** Mandatory use of Python type hints for all functions, methods, and class attributes. No implicit types allowed.
- **Readability First:** Code should be self-documenting. Use clear variable names, function names, and class names that express intent.
- **Single Responsibility:** Each function/class should have one clear purpose. No god objects or multi-purpose utilities.
- **DRY Principle:** Don't Repeat Yourself. Extract common logic into reusable functions or classes.

### II. Architecture & Separation of Concerns

- **Layer Separation:** Clear separation between UI (CLI) and Logic (Task Manager Core).
  - **CLI Layer:** Handles user interaction, input parsing, output formatting
  - **Logic Layer:** Task management operations (CRUD), validation, business rules
  - **Data Layer:** In-memory storage management (dictionaries/lists)
- **Object-Oriented Design (Preferred):** Use classes to encapsulate task entities and manager logic.
- **No Business Logic in UI:** CLI should only orchestrate calls to logic layer, never implement business rules directly.
- **Testable Design:** All logic must be independently testable without CLI interaction.

### III. Test-First Development (NON-NEGOTIABLE)

- **TDD Mandatory:** Tests written → User approved → Tests fail → Then implement
- **Red-Green-Refactor cycle strictly enforced:**
  1. Write failing test
  2. Write minimal code to pass test
  3. Refactor while keeping tests green
- **Test Coverage Requirements:**
  - All CRUD operations (Add, View, Update, Delete, Mark Complete)
  - Edge cases: invalid IDs, empty inputs, duplicate operations
  - Error handling paths
- **Test Organization:** Tests should mirror source structure and be clearly named (e.g., `test_add_task_success`, `test_delete_task_invalid_id`)

### IV. Error Handling & Validation

- **Graceful Degradation:** Never crash on user input. All errors should be caught and communicated clearly.
- **Input Validation:** Validate all user inputs before processing:
  - Task IDs must exist before update/delete/mark operations
  - Title and description must be non-empty for add operations
  - Type validation for all function parameters
- **Error Messages:** Clear, actionable error messages that guide users to correct usage.
- **Exception Hierarchy:** Use custom exceptions for domain-specific errors (e.g., `TaskNotFoundError`, `InvalidTaskDataError`)

### V. User Experience & Interface Design

- **Clean CLI Output:** Well-formatted, readable output with clear status indicators:
  - `[ ]` for pending tasks
  - `[x]` for completed tasks
- **Consistent Command Structure:** Intuitive command patterns that follow CLI best practices
- **Helpful Feedback:** Confirmation messages for all operations (e.g., "Task #3 deleted successfully")
- **User-Friendly Prompts:** Clear prompts that explain what input is expected

### VI. Simplicity & YAGNI

- **Start Simple:** Implement only as five core requirements for Phase I:
  1. Add Task
  2. View Tasks
  3. Update Task
  4. Delete Task
  5. Mark Task as Complete
- **No Over-Engineering:** Don't build features for future phases. No database abstractions, no API layers, no complex frameworks.
- **YAGNI (You Aren't Gonna Need It):** Only build what's explicitly required. No speculative features.
- **Incremental Complexity:** Add complexity only when requirements demand it.

## Phase I Technology Stack & Constraints

### Mandatory Technologies

- **Python Version:** 3.13+ (Utilize latest language features and syntax)
- **Package Manager:** uv (Fast Python package installer and resolver)
- **Testing Framework:** pytest (industry standard, powerful fixtures)
- **Type Checking:** mypy (static type checker for Python)
- **Linting:** ruff or flake8 (PEP 8 compliance verification)

### Phase I Constraints

- **Storage:** In-memory only (Python dictionaries/lists). No file I/O, no databases.
- **Interface:** CLI only. No GUI, no web interface.
- **Dependencies:** Minimal external dependencies. Prefer standard library when possible.
- **Deployment:** Local execution only. No containerization or cloud deployment in Phase I.

### Forbidden in Phase I

- External databases (SQLite, PostgreSQL, etc.)
- File persistence (JSON, CSV, pickle)
- Web frameworks (Flask, FastAPI, Django)
- Complex ORMs or data mapping libraries
- Async/await patterns (unless clearly beneficial for CLI)

## Phase I Development Workflow

### Code Quality Gates

All code must pass these gates before being considered complete:

1. **Type Checking:** `mypy` runs without errors
2. **Linting:** `ruff` or `flake8` passes with zero warnings
3. **Tests:** All pytest tests pass with 100% success rate
4. **Coverage:** Minimum 80% code coverage for core logic
5. **Manual Testing:** CLI operations verified through manual testing

### Phase I Development Cycle

1. **Specification:** Define feature requirements and acceptance criteria
2. **Test Design:** Write comprehensive test cases
3. **Test Implementation:** Implement failing tests
4. **Code Implementation:** Write minimal code to pass tests
5. **Refactoring:** Improve code quality while maintaining green tests
6. **Documentation:** Update docstrings and comments
7. **Manual Verification:** Test CLI end-to-end

### Code Review Standards

- All functions have type hints
- All public functions have docstrings (Google or NumPy style)
- No magic numbers or hardcoded strings (use constants)
- Error handling covers expected failure modes
- Tests cover both happy path and error cases

## Phase I Core Feature Requirements

### 1. Add Task
- **Input:** Title (required, non-empty string), Description (required, non-empty string)
- **Output:** Unique task ID (auto-generated), confirmation message
- **Validation:** Title and description cannot be empty or whitespace-only
- **ID Generation:** Sequential integers starting from 1, or UUID for uniqueness

### 2. View Tasks
- **Input:** None (displays all tasks)
- **Output:** Formatted list of all tasks with:
  - Task ID
  - Title
  - Description
  - Status indicator (`[ ]` pending, `[x]` complete)
- **Edge Cases:** Handle empty task list gracefully

### 3. Update Task
- **Input:** Task ID (required), new title (optional), new description (optional)
- **Output:** Confirmation message with updated task details
- **Validation:** Task ID must exist, at least one field must be updated
- **Error Handling:** Clear error for non-existent IDs

### 4. Delete Task
- **Input:** Task ID (required)
- **Output:** Confirmation message
- **Validation:** Task ID must exist
- **Error Handling:** Clear error for non-existent IDs

### 5. Mark Task as Complete/Toggle Status
- **Input:** Task ID (required)
- **Output:** Confirmation message with new status
- **Validation:** Task ID must exist
- **Behavior:** Toggle between pending and complete states

## Code Standards & Best Practices

### Naming Conventions

- **Classes:** PascalCase (e.g., `TaskManager`, `Task`)
- **Functions/Methods:** snake_case (e.g., `add_task`, `get_task_by_id`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `MAX_TITLE_LENGTH`, `DEFAULT_STATUS`)
- **Private Members:** Leading underscore (e.g., `_tasks`, `_generate_id`)

### Documentation Requirements

- **Module Docstrings:** Every module file must have a docstring explaining its purpose
- **Class Docstrings:** Describe class responsibility and key attributes
- **Function Docstrings:** Include:
  - Brief description
  - Parameters with types
  - Return value with type
  - Raises (exceptions that can be thrown)
  - Example usage (for complex functions)

### Type Hinting Examples

```python
from typing import Optional, Dict, List

def add_task(title: str, description: str) -> int:
    """Add a new task and return its ID."""
    pass

def get_task(task_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve task by ID, return None if not found."""
    pass

def list_tasks() -> List[Dict[str, Any]]:
    """Return all tasks as a list of dictionaries."""
    pass
```

### Error Handling Patterns

```python
class TaskNotFoundError(Exception):
    """Raised when a task ID doesn't exist."""
    pass

class InvalidTaskDataError(Exception):
    """Raised when task data is invalid."""
    pass

def delete_task(task_id: int) -> None:
    if task_id not in tasks:
        raise TaskNotFoundError(f"Task {task_id} not found")
    # ... deletion logic
```

---

# PHASE II: FULL-STACK WEB APPLICATION

## Core Principles

### VII. Monorepo Structure (NON-NEGOTIABLE)

- **Structured Monorepo:** Project MUST follow structured monorepo pattern to allow Claude Code to manage both stacks simultaneously:
  ```
  hackathon-todo/
  ├── .spec-kit/
  ├── specs/
  ├── CLAUDE.md
  ├── frontend/  (Next.js app)
  ├── backend/   (FastAPI app)
  ├── docker-compose.yml
  └── README.md
  ```
- **Independent Stacks:** Frontend and backend are independently deployable services
- **Clear Boundaries:** No cross-stack dependencies except via well-defined API contracts
- **Spec-Driven Architecture:** All code changes must be initiated by updating spec files

### VIII. API-First Design

- **RESTful Contracts:** All interactions between frontend and backend via REST API
- **OpenAPI/Swagger:** Backend MUST provide API documentation at `/docs`
- **Pydantic Validation:** All request/response models MUST use Pydantic for type safety
- **Versioning:** API versioning via `/api/v1/` prefix (future-proof)
- **Error Standardization:** Consistent error response format across all endpoints

### IX. Stateless Authentication (NON-NEGOTIABLE)

- **JWT Tokens:** All API requests must include valid JWT token in `Authorization: Bearer <token>` header
- **Better Auth (Frontend):** Configure Better Auth to issue JWT tokens on login
- **Shared Secret:** Frontend (Better Auth) and backend (FastAPI) MUST use same `BETTER_AUTH_SECRET`
- **Token Expiry:** JWT tokens expire automatically (e.g., after 7 days)
- **User Isolation:** Backend filters ALL queries by authenticated user's ID

### X. Security & Authorization

- **401 on Missing Token:** Requests without JWT token receive 401 Unauthorized
- **User Ownership Enforcement:** Each user only sees/modifies their own tasks
- **Middleware Verification:** FastAPI MUST intercept requests, verify JWT, extract user_id
- **No Direct Database Access:** Frontend never connects directly to database
- **Secrets Management:** Never hardcode secrets. Use environment variables (`BETTER_AUTH_SECRET`, `DATABASE_URL`)

### XI. Spec-Driven Development (NON-NEGOTIABLE)

- **Spec First:** Write/update specs BEFORE any code implementation
  - `specs/database/schema.md` - Database schema
  - `specs/api/rest-endpoints.md` - API contracts
  - `specs/ui/components.md` - UI components
- **No Manual Boilerplate:** Refine specifications until AI generates correct implementation
- **Contract Tests:** API endpoints MUST have contract tests
- **Incremental Specs:** Update specs as architecture evolves

### XII. Multi-User Persistence

- **User Association:** All tasks MUST be associated with `user_id`
- **Serverless Database:** Neon PostgreSQL (serverless, auto-scaling)
- **ORM Integration:** SQLModel for Pydantic/SQL integration
- **Migration Support:** Database migrations must be version-controlled
- **Data Integrity:** Foreign key constraints, indexes, proper relationships

## Phase II Technology Stack & Constraints

### Mandatory Technologies

**Frontend Stack:**
- **Framework:** Next.js 16+ (App Router)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS
- **Authentication:** Better Auth
- **Package Manager:** npm or pnpm

**Backend Stack:**
- **Framework:** Python, FastAPI
- **ORM:** SQLModel (Pydantic + SQLAlchemy)
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** JWT token verification
- **Package Manager:** uv

**Infrastructure:**
- **Orchestration:** Docker Compose (local development)
- **Version Control:** Git with structured monorepo

### Phase II Constraints

- **Monorepo Structure:** MUST follow frontend/backend separation
- **API Communication:** Frontend ↔ Backend via REST API only
- **Database Access:** Only backend accesses Neon PostgreSQL
- **Authentication Flow:** Better Auth issues JWT → Backend verifies JWT → Extracts user_id
- **Type Safety:** 100% type hinting in Python, strict TypeScript
- **No Manual Code:** All code changes via spec updates or prompts

### Forbidden in Phase II

- Direct frontend-to-database connections
- Session-based authentication (stateless JWT required)
- Hardcoded credentials or secrets
- Mixed frontend/backend code in same directory
- Skipping JWT verification on any endpoint

## Phase II API Endpoints

All endpoints require valid JWT token in `Authorization: Bearer <token>` header:

| Method | Endpoint | Description |
|---------|-----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user |
| POST | `/api/{user_id}/tasks` | Create new task for user |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle task completion |

**Security Requirements:**
- Extract `user_id` from decoded JWT
- Match `user_id` in URL with authenticated user
- Return 403 if user attempts to access another user's data
- Filter all database queries by `user_id`

## Phase II Development Workflow

### Code Quality Gates

All code must pass these gates:

**Backend (Python):**
1. **Type Checking:** `mypy` runs without errors
2. **Linting:** `ruff` passes with zero warnings
3. **Tests:** All pytest tests pass with 100% success rate
4. **Coverage:** Minimum 80% code coverage
5. **API Validation:** Swagger UI docs available at `/docs`

**Frontend (TypeScript):**
1. **Type Checking:** TypeScript strict mode passes
2. **Linting:** ESLint passes with zero errors
3. **Formatting:** Prettier consistent formatting
4. **Tests:** All tests pass (if applicable)
5. **Build:** `npm run build` succeeds

### Phase II Execution Workflow

1. **Spec First:** Write `specs/database/schema.md` and `specs/api/rest-endpoints.md`
2. **Infrastructure:** Initialize Neon DB and link to FastAPI backend
3. **Logic:** Implement Backend CRUD logic and test with Swagger UI (`/docs`)
4. **Frontend:** Build Next.js UI and integrate Better Auth
5. **Integration:** Connect UI to API via centralized fetch client
6. **Authentication:** Configure Better Auth JWT issuance + FastAPI JWT verification
7. **Security:** Verify user isolation across all operations

### Code Review Standards

- All functions have type hints (Python) or type annotations (TypeScript)
- All Pydantic models properly validated
- JWT verification on ALL endpoints
- User_id filtering in ALL database queries
- No hardcoded secrets or tokens
- API contracts match specification

## Phase II Core Requirements

### 1. Multi-User Support

- **Task Ownership:** Every task MUST have `user_id` foreign key
- **User Isolation:** Users only see their own tasks
- **JWT-based User ID:** Extract user ID from decoded JWT token
- **URL Validation:** Match `user_id` in URL path with authenticated user

### 2. RESTful API

- **CRUD Operations:** Implement GET, POST, PUT, DELETE, and PATCH (for completion)
- **Pydantic Models:** Separate models for requests and responses
- **Error Responses:** Consistent JSON error format with status codes
- **OpenAPI Docs:** Auto-generated Swagger documentation at `/docs`

### 3. Authentication

- **JWT Token Issuance:** Better Auth issues JWT on user login
- **JWT Verification:** FastAPI middleware verifies token on every request
- **Shared Secret:** Both services use `BETTER_AUTH_SECRET` environment variable
- **Token Expiry:** Automatic expiration (e.g., 7 days)
- **401 Unauthorized:** Return 401 for missing or invalid tokens

### 4. Database Integration

- **Neon PostgreSQL:** Serverless PostgreSQL database
- **SQLModel ORM:** Pydantic models that double as SQL tables
- **Migrations:** Version-controlled database migrations
- **Connection Pooling:** Efficient connection management
- **Environment Config:** `DATABASE_URL` from environment variables

## Coding Standards (Phase II)

### Python Standards

- **Clean Code:** PEP 8 compliance
- **Type Safety:** 100% type hinting
- **Pydantic Models:** All request/response schemas as Pydantic models
- **FastAPI Dependency Injection:** Use `Depends()` for database sessions, auth
- **Error Handling:** Custom exception handlers with proper status codes

### TypeScript Standards

- **Strict Mode:** `strict: true` in tsconfig.json
- **Type Safety:** No `any` types unless absolutely necessary
- **Component Props:** Explicit interface for all component props
- **API Client:** Type-safe fetch wrapper with TypeScript types
- **ESLint + Prettier:** Consistent formatting and linting

### API Conventions

- **JSON Responses:** All endpoints return JSON
- **HTTP Status Codes:** Proper status codes (200, 201, 400, 401, 404, 500)
- **Request Validation:** Pydantic models validate input before processing
- **Error Messages:** Clear, actionable error messages
- **Versioning:** `/api/v1/` prefix for future compatibility

---

# Governance

### Constitution Authority

- This constitution supersedes all other development practices and guidelines
- All code, tests, and documentation must comply with these principles
- Deviations require explicit justification and documented approval
- Phase I principles apply to CLI code; Phase II principles apply to full-stack code

### Amendment Process

- Constitution amendments must be documented in project history
- Significant changes require ADR (Architecture Decision Record)
- Version number must be incremented for all amendments
  - MAJOR: Backward incompatible governance/principle removals
  - MINOR: New principle/section added or materially expanded guidance
  - PATCH: Clarifications, wording, typo fixes

### Compliance Verification

- All pull requests must verify compliance with constitution principles
- Code reviews must reference specific constitution sections when rejecting code
- For Phase I: Complexity must be justified against Simplicity principle (VI)
- For Phase II: Code changes must follow spec-driven workflow (XI)

### Escalation Path

**Phase I Conflicts** (prioritize in this order):
1. Test-First Development (III)
2. Clean Code & Maintainability (I)
3. Simplicity & YAGNI (VI)
4. Architecture & Separation of Concerns (II)
5. Error Handling & Validation (IV)
6. User Experience & Interface Design (V)

**Phase II Conflicts** (prioritize in this order):
1. Stateless Authentication (IX)
2. Security & Authorization (X)
3. Spec-Driven Development (XI)
4. Multi-User Persistence (XII)
5. Monorepo Structure (VII)
6. API-First Design (VIII)

**Cross-Phase Conflicts:**
When Phase I and Phase II principles conflict, prioritize the phase relevant to the code being written. CLI code follows Phase I; full-stack code follows Phase II.

**Version**: 2.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-29
