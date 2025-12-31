---

description: "Task list template for feature implementation"
---

# Tasks: Phase II Full-Stack Web Application

**Input**: Design documents from `/specs/002-full-stack-web/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in feature specification.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web application**: `backend/src/`, `frontend/src/`
- Paths shown below assume monorepo structure - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are generated from plan.md and spec.md

  Task organization:
  - Phase 1: Setup (project initialization)
  - Phase 2: Foundational (blocking prerequisites)
  - Phase 3: User Story 1 (Registration & Login)
  - Phase 4: User Story 2 (Create & Manage Tasks)
  - Phase 5: User Story 3 (User Data Isolation)
  - Phase 6: Polish & Cross-Cutting Concerns
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

- [x] T001 Initialize root monorepo structure with backend/ and frontend/ directories
- [x] T002 Create root .env.example with BETTER_AUTH_SECRET and DATABASE_URL placeholders
- [ ] T003 Create docker-compose.yml for local development orchestration
- [ ] T004 Update root README.md with monorepo setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [x] T005 Initialize backend/ with uv and pyproject.toml
- [x] T006 [P] Install backend dependencies: fastapi, uvicorn, sqlmodel, psycopg2-binary, pyjwt
- [x] T007 [P] Create backend/src/ directory structure (models/, api/, tests/)
- [x] T008 Configure .env.example with DATABASE_URL placeholder

### Frontend Foundation

- [ ] T009 Initialize frontend/ with Next.js (create-next-app)
- [ ] T010 [P] Install frontend dependencies: better-auth, tailwindcss
- [ ] T011 [P] Configure TypeScript strict mode in tsconfig.json
- [ ] T012 [P] Setup Tailwind CSS configuration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Login (Priority: P1) 🎯 MVP

**Goal**: Implement user authentication flow with Better Auth and JWT token issuance

**Independent Test**: Can be fully tested by registering a new account, logging in, and verifying session creation with JWT token

### Implementation for User Story 1

- [ ] T013 [US1] Configure Better Auth with email provider in frontend/src/app/auth.tsx
- [ ] T014 [US1] Implement login page (/) in frontend/src/app/page.tsx
- [ ] T015 [US1] Implement logout functionality in Navbar component
- [ ] T016 [US1] Create get_current_user dependency in backend/src/api/dependencies.py
- [ ] T017 [US1] Implement JWT decode function using PyJWT in backend/src/api/dependencies.py
- [ ] T018 [US1] Verify BETTER_AUTH_SECRET from environment variables
- [ ] T019 [US1] Create HTTPException for 401 Unauthorized in backend/src/api/dependencies.py
- [ ] T020 [US1] Store JWT token in frontend session/localStorage

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Create and Manage Tasks (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create new tasks, view their task list, update task details, and delete tasks

**Independent Test**: Can be fully tested by creating a task, viewing it, editing it, and deleting it within one user session

### Backend Data Layer (US2)

- [x] T021 [P] [US2] Create Task SQLModel in backend/src/models/task.py
- [x] T022 [P] [US2] Add user_id foreign key field to Task model
- [x] T023 [P] [US2] Add validation rules (title: 1-200 chars, description: max 1000 chars)
- [x] T024 [P] [US2] Add indexes (user_id, created_at) for performance
- [ ] T025 [US2] Create database engine configuration in backend/src/api/dependencies.py
- [ ] T026 [US2] Create database migration script for Task table

### Backend Authentication Layer (US2)

- [ ] T027 [US2] Add HTTPException for 403 Forbidden in backend/src/api/dependencies.py

### Backend API Routes - Tasks (US2)

- [ ] T028 [P] [US2] Create backend/src/api/routes/tasks.py with task router
- [ ] T029 [US2] Implement GET /api/tasks - list tasks filtered by user_id
- [ ] T030 [US2] Implement POST /api/tasks - create task with user_id
- [ ] T031 [US2] Implement GET /api/tasks/{id} - get task with ownership check
- [ ] T032 [US2] Implement PUT /api/tasks/{id} - update task with ownership check
- [ ] T033 [US2] Implement PATCH /api/tasks/{id}/complete - toggle completion
- [ ] T034 [US2] Implement DELETE /api/tasks/{id} - delete with ownership check
- [ ] T035 [US2] Add Pydantic request/response models to backend/src/api/routes/tasks.py
- [ ] T036 [US2] Include routes in backend/src/api/main.py
- [ ] T037 [US2] Add OpenAPI documentation (automatic via FastAPI)

### Frontend API Client (US2)

- [ ] T038 [P] [US2] Create fetch wrapper in frontend/src/app/lib/api.ts
- [ ] T039 [US2] Add JWT token to Authorization header on all requests
- [ ] T040 [P] [US2] Add TypeScript types for API requests/responses
- [ ] T041 [US2] Implement error handling (401, 403, 404)

### Frontend UI Components (US2)

- [ ] T042 [P] [US2] Create Navbar component with logout button in frontend/src/app/components/Navbar.tsx
- [ ] T043 [P] [US2] Create TaskForm component (modal/inline) in frontend/src/app/components/TaskForm.tsx
- [ ] T044 [P] [US2] Create TaskList component in frontend/src/app/components/TaskList.tsx
- [ ] T045 [P] [US2] Create TaskItem component with status toggle and delete in frontend/src/app/components/TaskItem.tsx

### Frontend Pages (US2)

- [ ] T046 [US2] Create dashboard page (/dashboard) in frontend/src/app/dashboard/page.tsx
- [ ] T047 [US2] Add middleware for JWT token verification on protected routes

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - User Data Isolation (Priority: P1) 🎯 MVP

**Goal**: Users only see and interact with their own tasks - they cannot access or modify tasks belonging to other users

**Independent Test**: Can be fully tested by logging in as User A, creating tasks, then logging out and logging in as User B - User B should never see User A's tasks

### Implementation for User Story 3

**Backend Routes - Already Implemented in US2**:
- [ ] T048 [US3] Verify all API routes filter queries by user_id (ownership check)
- [ ] T049 [US3] Verify 403 Forbidden returned for cross-user access attempts

**Frontend API Client - Already Implemented in US2**:
- [ ] T050 [US3] Verify error handling for 403 Forbidden in api.ts

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Backend Polish

- [ ] T051 Update backend/README.md with setup instructions
- [ ] T052 Create backend/src/api/main.py FastAPI app setup
- [ ] T053 Configure CORS middleware for frontend origin in backend/src/api/main.py
- [ ] T054 Setup logging configuration in backend/src/api/main.py

### Frontend Polish

- [ ] T055 Update frontend/README.md with setup instructions
- [ ] T056 Implement loading states in components
- [ ] T057 Implement error handling display in components
- [ ] T058 Create root layout with Navbar in frontend/src/app/layout.tsx

### Documentation

- [ ] T059 Document environment variables in root README.md
- [ ] T060 Document deployment process in root README.md

### Code Quality

- [ ] T061 Run mypy on backend (0 errors)
- [ ] T062 Run ruff on backend (0 warnings)
- [ ] T063 Run TypeScript strict check on frontend
- [ ] T064 Run ESLint on frontend (0 errors)
- [ ] T065 Format all code (Prettier on frontend, ruff format on backend)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - User Story 2 (Phase 4): Can start after Foundational - No dependencies on other stories
  - User Story 3 (Phase 5): Can start after Foundational - No dependencies on other stories
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Stories 1-2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Registration & Login)
4. Complete Phase 4: User Story 2 (Create & Manage Tasks)
5. **STOP and VALIDATE**: Test User Stories 1 & 2 independently
6. Deploy/Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP core!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Phase 3)
   - Developer B: User Story 2 (Phase 4)
   - Developer C: User Story 3 (Phase 5)
3. Stories complete and integrate independently
4. Together complete polish and deployment (Phase 6)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if tests included)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

**Total Tasks**: 65
- Phase 1: 4 tasks (Setup)
- Phase 2: 8 tasks (Foundational - backend/frontend)
- Phase 3: 8 tasks (US1 - Registration & Login)
- Phase 4: 24 tasks (US2 - Create & Manage Tasks)
- Phase 5: 3 tasks (US3 - Data Isolation - verification)
- Phase 6: 18 tasks (Polish & Cross-Cutting)

**Parallel Opportunities**: 33 tasks marked [P] can run in parallel

**Independent Test Criteria**:
- US1: Register account, login, verify JWT token
- US2: Create task, view tasks, update task, delete task
- US3: User A creates tasks, logs out, User B logs in → User B never sees User A's tasks
