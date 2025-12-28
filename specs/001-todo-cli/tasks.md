# Tasks: In-Memory Todo CLI Application

**Input**: Design documents from `/specs/001-todo-cli/`

**Prerequisites**: plan.md, spec.md, data-model.md

**Tests**: Included (constitution mandates TDD approach)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

---

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure per implementation plan (src/todo_cli/models/, src/todo_cli/core/, src/todo_cli/cli/, tests/unit/, tests/integration/)

- [X] T002 Initialize Python 3.13+ project with uv package manager

- [X] T003 [P] Create pyproject.toml with project metadata and tool configuration (pytest, mypy, ruff)

- [X] T004 [P] Create mypy.ini for type checking configuration with strict mode

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create custom exception hierarchy in src/todo_cli/core/exceptions.py (TodoError, TaskNotFoundError, InvalidTaskDataError)

- [X] T006 [P] Create Task dataclass in src/todo_cli/models/task.py with validation in __post_init__

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks with titles and descriptions, and view all tasks in a clear, readable format

**Independent Test**: Launch application, add tasks, view task list to verify correct display with status indicators

### Tests for User Story 1 (TDD - write these FIRST)

- [X] T007 [P] [US1] Write unit test for Task dataclass creation and validation in tests/unit/test_task_model.py

- [X] T008 [P] [US1] Write unit tests for TaskManager add_task, view_tasks, get_task methods in tests/unit/test_task_manager.py

- [X] T009 [P] [US1] Write unit test for task formatting (status indicators, truncation, wrapping) in tests/unit/test_formatter.py

- [X] T010 [P] [US1] Write integration test for add task flow (create task, view in list) in tests/integration/test_cli_flows.py

- [X] T011 [P] [US1] Write integration test for view tasks with empty list (show friendly message) in tests/integration/test_cli_flows.py

### Implementation for User Story 1

- [X] T012 [US1] Implement TaskManager add_task method in src/todo_cli/core/task_manager.py (generate sequential ID, validate data, store in dict)

- [X] T013 [US1] Implement TaskManager view_tasks method in src/todo_cli/core/task_manager.py (return List[Task])

- [X] T014 [US1] Implement TaskManager get_task method in src/todo_cli/core/task_manager.py (raise TaskNotFoundError if not found)

- [X] T015 [US1] Implement CLI formatter in src/todo_cli/cli/formatter.py (format task display with status indicators `[ ]`/`[x]`, truncate long text)

- [X] T016 [US1] Implement CLI interface menu in src/todo_cli/cli/interface.py (show menu, handle Add Task and View Tasks options)

- [X] T017 [US1] Create application entry point in src/todo_cli/__main__.py (main loop, import and call interface)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP complete)

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Enable users to toggle task completion status between pending and complete

**Independent Test**: Create task, toggle completion status, verify status indicator changes from `[ ]` to `[x]` and vice versa

### Tests for User Story 2

- [X] T018 [P] [US2] Write unit tests for TaskManager toggle_status method in tests/unit/test_task_manager.py (toggle pending→complete, toggle complete→pending, error on invalid ID)

- [X] T019 [P] [US2] Write integration test for toggle complete flow (add task, toggle, view to verify change) in tests/integration/test_cli_flows.py

### Implementation for User Story 2

- [X] T020 [US2] Implement TaskManager toggle_status method in src/todo_cli/core/task_manager.py (flip is_complete boolean, return updated Task)

- [X] T021 [US2] Add Toggle Complete menu option to CLI interface in src/todo_cli/cli/interface.py (handle input, call toggle_status, display confirmation)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable users to modify existing task titles and descriptions

**Independent Test**: Create task, update title and/or description, verify changes reflected in task list

### Tests for User Story 3

- [X] T022 [P] [US3] Write unit tests for TaskManager update_task method in tests/unit/test_task_manager.py (update title only, update description only, update both, error on invalid ID, error on empty title)

- [X] T023 [P] [US3] Write integration test for update task flow (create task, update, view to verify changes) in tests/integration/test_cli_flows.py

### Implementation for User Story 3

- [X] T024 [US3] Implement TaskManager update_task method in src/todo_cli/core/task_manager.py (validate ID exists, validate new data if provided, update task attributes, return updated Task)

- [X] T025 [US3] Add Update Task menu option to CLI interface in src/todo_cli/cli/interface.py (handle input, prompt for title/description, call update_task, display confirmation)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable users to remove tasks they no longer need

**Independent Test**: Create tasks, delete one by ID, verify it no longer appears in task list

### Tests for User Story 4

- [X] T026 [P] [US4] Write unit tests for TaskManager delete_task method in tests/unit/test_task_manager.py (delete existing task, error on invalid ID, verify task removed from storage)

- [X] T027 [P] [US4] Write integration test for delete task flow (create tasks, delete, view to verify removal, verify ID not reused) in tests/integration/test_cli_flows.py

### Implementation for User Story 4

- [X] T028 [US4] Implement TaskManager delete_task method in src/todo_cli/core/task_manager.py (validate ID exists, remove from dict, no ID reuse)

- [X] T029 [US4] Add Delete Task menu option to CLI interface in src/todo_cli/cli/interface.py (handle input, call delete_task, display confirmation, show empty list message if applicable)

- [X] T030 [US4] Add Exit option to CLI interface in src/todo_cli/cli/interface.py (terminate loop, display data loss warning)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T031 [P] Add data loss warning on application startup in src/todo_cli/cli/interface.py (display on first menu show)

- [X] T032 [P] Add Exit confirmation prompt with reminder in src/todo_cli/cli/interface.py (warn that tasks will be lost)

- [X] T033 Run quickstart.md validation (follow setup guide, ensure all steps work as documented)

- [X] T034 Run mypy type checking on all source files (mypy src/todo_cli) - fix any errors

- [X] T035 Run ruff linting and formatting (ruff check src/todo_cli && ruff format src/todo_cli) - fix any issues

- [X] T036 Run pytest with coverage (pytest --cov=src/todo_cli --cov-report=term-missing) - ensure 80%+ coverage

- [X] T037 Create README.md with usage instructions, examples, and data loss warning

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - May integrate with US1 but should be independently testable
  - User Story 3 (P3): Can start after Foundational - May integrate with US1/US2 but should be independently testable
  - User Story 4 (P4): Can start after Foundational - May integrate with US1/US2/US3 but should be independently testable
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Should be independently testable (toggle status on tasks created by US1)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Should be independently testable (update tasks created by US1)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Should be independently testable (delete tasks created by US1)

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Tests (T007-T011, T018-T019, T022-T023, T026-T027) can run in parallel
- Models (T006) before services (T012, T020, T024, T028)
- Services (T012, T020, T024, T028) before interface integration (T016, T021, T025, T029)
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T001-T004) marked [P] can run in parallel
- All Foundational tasks (T005-T006) marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write unit test for Task dataclass creation and validation in tests/unit/test_task_model.py"
Task: "Write unit tests for TaskManager add_task, view_tasks, get_task methods in tests/unit/test_task_manager.py"
Task: "Write unit test for task formatting in tests/unit/test_formatter.py"
Task: "Write integration test for add task flow in tests/integration/test_cli_flows.py"
Task: "Write integration test for view tasks with empty list in tests/integration/test_cli_flows.py"

# Launch all models and services for User Story 1 together:
Task: "Implement TaskManager add_task method in src/todo_cli/core/task_manager.py"
Task: "Implement TaskManager view_tasks method in src/todo_cli/core/task_manager.py"
Task: "Implement TaskManager get_task method in src/todo_cli/core/task_manager.py"
Task: "Implement CLI formatter in src/todo_cli/cli/formatter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T006) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T007-T017) - tests first, then implementation
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Run quickstart.md setup guide as verification
6. Demo MVP (add and view tasks only)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo/Deploy (MVP!)
3. Add User Story 2 → Test independently → Demo/Deploy
4. Add User Story 3 → Test independently → Demo/Deploy
5. Add User Story 4 → Test independently → Demo/Deploy
6. Complete Polish phase → Final delivery
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T006)
2. Once Foundational is done:
   - Developer A: User Story 1 (T007-T017)
   - Developer B: User Story 2 (T018-T021)
   - Developer C: User Story 3 (T022-T025)
3. Stories complete and integrate independently
4. Team completes Polish phase together (T031-T037)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Total tasks: 37
- Tasks per user story:
  - US1 (P1): 11 tasks (5 tests, 6 implementation)
  - US2 (P2): 4 tasks (2 tests, 2 implementation)
  - US3 (P3): 4 tasks (2 tests, 2 implementation)
  - US4 (P4): 5 tasks (2 tests, 3 implementation)
- Parallel tasks (marked [P]): 18 total
