# Implementation Plan: In-Memory Todo CLI Application

**Branch**: `001-todo-cli` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli/spec.md`

## Summary

Implement an in-memory CLI todo application with five core operations (add, view, update, delete, toggle completion). Built with Python 3.13+ using modern practices (dataclasses, type hints) and TDD methodology. Architecture follows three-layer separation (CLI → Logic → Data) with clear test boundaries and quality gates enforced by mypy, ruff, and pytest.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: pytest, mypy, ruff (development tools only)
**Storage**: In-memory Dict[int, Task] (no persistence)
**Testing**: pytest with unit + integration tests
**Target Platform**: Cross-platform (Windows, macOS, Linux)
**Project Type**: Single project (CLI application)
**Performance Goals**: O(1) CRUD operations, <10ms response for user interactions
**Constraints**: <1MB memory footprint (negligible for 50 tasks), offline-capable (no network dependencies)
**Scale/Scope**: Single user, single session, ~50 tasks max per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Initial Check (Pre-Design)

| Principle | Requirement | Status |
|-----------|------------|--------|
| I. Clean Code & Maintainability | PEP 8, type hints, readable code | ✅ Gates in plan |
| II. Architecture & Separation | 3-layer design (CLI/Logic/Data) | ✅ Structure defined |
| III. Test-First Development | TDD with pytest, 80%+ coverage | ✅ Test strategy documented |
| IV. Error Handling & Validation | Custom exceptions, input validation | ✅ Exception hierarchy planned |
| V. User Experience | Clear prompts, status indicators | ✅ Formatter module planned |
| VI. Simplicity & YAGNI | 5 core ops only, no over-engineering | ✅ Minimal scope |

**Status**: ✅ PASS - All gates satisfied before Phase 0

### Post-Design Check (After Phase 1)

| Principle | Design Validation | Status |
|-----------|------------------|--------|
| I. Clean Code | dataclass for Task, mypy strict enforced | ✅ Pass |
| II. Separation | models/, core/, cli/ directories | ✅ Pass |
| III. Test-First | Unit tests for TaskManager, integration for CLI | ✅ Pass |
| IV. Error Handling | TodoError hierarchy with specific exceptions | ✅ Pass |
| V. UX | Status indicators `[ ]`/`[x]`, formatted output | ✅ Pass |
| VI. Simplicity | Dict[int, Task], no external runtime deps | ✅ Pass |

**Status**: ✅ PASS - No violations, all design choices align with constitution

**Conclusion**: No complexity tracking needed - all design decisions follow constitution principles without requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - Technical decisions
├── data-model.md        # Phase 1 output - Task entity definition
├── quickstart.md        # Phase 1 output - Setup guide
└── checklists/
    └── requirements.md   # Specification quality checklist
```

### Source Code (repository root)

```text
todo-cli/
├── src/
│   └── todo_cli/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Entry point (python -m todo_cli)
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py          # Task dataclass (Data Layer)
│       ├── core/
│       │   ├── __init__.py
│       │   ├── exceptions.py     # TodoError hierarchy
│       │   └── task_manager.py   # CRUD operations (Logic Layer)
│       └── cli/
│           ├── __init__.py
│           ├── formatter.py      # Output formatting
│           └── interface.py      # Menu and user interaction (CLI Layer)
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task_model.py       # Task dataclass tests
│   │   ├── test_task_manager.py     # TaskManager CRUD tests
│   │   └── test_formatter.py        # Formatting tests
│   └── integration/
│       ├── __init__.py
│       └── test_cli_flows.py        # End-to-end user scenarios
├── pyproject.toml               # Project metadata and tooling config
├── mypy.ini                     # Type checking configuration
└── README.md                    # User documentation
```

**Structure Decision**: Single project structure with three-layer separation (models/, core/, cli/). Each layer has distinct responsibility and testability. No web or mobile components detected in spec, so Option 1 (single project) is chosen.

## Complexity Tracking

> **No violations to justify** - All design choices align with constitution principles without requiring complexity.

| N/A | N/A | N/A |
|-----|-----|-----|

## Design Decisions & Rationale

### Data Model

**Decision**: Use Python `@dataclass` for Task entity

**Rationale**:
- Built-in feature (Python 3.7+), no external dependencies
- Automatic `__init__`, `__repr__`, `__eq__` generation
- Type hints integrated naturally
- Validates against constitution's mandatory type hinting

**Implementation**: See `data-model.md` for full specification

### Storage Strategy

**Decision**: Dict[int, Task] in TaskManager with sequential ID counter

**Rationale**:
- O(1) lookup for update/delete/toggle operations
- User-friendly sequential IDs (1, 2, 3...)
- Simple, no need for complex data structures
- Aligns with spec requirement for sequential integer IDs

**Trade-offs**:
- List[Task] would work but O(n) lookup rejected for performance
- OrderedDict unnecessary - dict maintains insertion order in Python 3.7+

### Validation Approach

**Decision**: Custom exception hierarchy with validation in logic layer

**Rationale**:
- Constitution mandates custom exceptions
- Centralized validation in TaskManager, not CLI
- Clear error types for specific failure modes
- Testable validation logic independent of user interface

**Exception Hierarchy**:
```python
TodoError (base)
├── TaskNotFoundError (for invalid task IDs)
└── InvalidTaskDataError (for empty/invalid inputs)
```

### Testing Strategy

**Decision**: pytest with unit + integration split

**Rationale**:
- Constitution mandates pytest
- Unit tests: Fast, isolated testing of TaskManager and Task
- Integration tests: End-to-end validation of user scenarios
- Mirrors source structure for maintainability

**Coverage Targets**:
- Unit tests: All TaskManager methods, edge cases
- Integration tests: All 4 user stories from spec
- Minimum coverage: 80% for core logic (constitution requirement)

### Project Tooling

**Type Checking**: mypy (strict mode)
- Enforces mandatory type hints
- Catches type errors before runtime
- Aligns with "Type Hinting: Mandatory" principle

**Linting**: ruff
- Fast PEP 8 compliance checking
- Auto-formatting capability
- Consistent code style across team

**Dependencies**: Minimal (development only)
- pytest: Testing framework (constitution-mandated)
- pytest-cov: Coverage reporting
- mypy: Type checking (constitution-mandated)
- ruff: Linting/formatting (constitution-mandated)

**Runtime**: Standard library only (no external packages)

## Phase 0: Research (Completed)

**Output**: `research.md` with all technical decisions resolved

**Research Topics Covered**:
1. Python 3.13+ project setup with uv
2. Project structure for CLI application
3. Data model implementation (dataclass vs alternatives)
4. In-memory storage strategy (Dict vs List)
5. ID generation approach (sequential integers)
6. Input validation approach (custom exceptions)
7. CLI menu design pattern
8. Testing strategy (pytest unit + integration)
9. Type checking configuration (mypy strict)
10. Code quality tools (ruff vs flake8)

**Status**: ✅ COMPLETE - All decisions documented and validated against constitution

## Phase 1: Design (Completed)

### 1.1 Data Model

**Output**: `data-model.md` with complete Task entity specification

**Contents**:
- Task attributes (id, title, description, is_complete)
- Validation rules (non-empty, non-whitespace)
- State machine (Pending ↔ Complete)
- Storage model (Dict[int, Task])
- Exception hierarchy
- Testing strategy

**Status**: ✅ COMPLETE

### 1.2 API Contracts

**N/A** - CLI application has no external API contracts

**Rationale**:
- Constitution mandates CLI-only interface for Phase I
- No web APIs or external integrations
- Internal contract: TaskManager methods (documented in data-model.md)

### 1.3 Quick Start Guide

**Output**: `quickstart.md` with developer onboarding instructions

**Contents**:
- Prerequisites (Python 3.13+, uv)
- Project setup steps
- Development workflow (TDD cycle)
- Common commands reference
- Quality gates checklist
- Troubleshooting guide

**Status**: ✅ COMPLETE

### 1.4 Agent Context Update

**Output**: `CLAUDE.md` updated with technology choices

**Changes**: Added Python 3.13+ to agent context for future interactions

**Status**: ✅ COMPLETE

## Architecture Overview

### Layer Architecture

```
┌─────────────────────────────────────────┐
│        CLI Layer (Presentation)        │
│  ┌──────────────────────────────┐  │
│  │  interface.py  (Menu & I/O)   │  │
│  │  formatter.py (Output format)  │  │
│  └──────────────┬───────────────┘  │
└─────────────────┼───────────────────┘
                  │ calls
┌─────────────────▼───────────────────┐
│      Logic Layer (TaskManager)        │
│  ┌──────────────────────────────┐  │
│  │  task_manager.py (CRUD)       │  │
│  │  exceptions.py (Error types)     │  │
│  └──────────────┬───────────────┘  │
└─────────────────┼───────────────────┘
                  │ stores
┌─────────────────▼───────────────────┐
│        Data Layer (Models)            │
│  ┌──────────────────────────────┐  │
│  │  task.py (Task dataclass)      │  │
│  └──────────────────────────────┘  │
└───────────────────────────────────────┘
```

### Data Flow

**Create Task Flow**:
1. User enters title/description via CLI menu
2. CLI (`interface.py`) validates basic input format
3. CLI calls `TaskManager.add_task(title, description)`
4. TaskManager validates non-empty strings
5. TaskManager generates sequential ID
6. TaskManager creates `Task` instance
7. TaskManager stores in `_tasks: Dict[int, Task]`
8. TaskManager returns Task to CLI
9. CLI (`formatter.py`) formats confirmation message
10. CLI displays formatted output to user

**View Tasks Flow**:
1. User selects "View Tasks" from menu
2. CLI calls `TaskManager.view_tasks()`
3. TaskManager returns `List[Task]`
4. CLI (`formatter.py`) formats each task with status indicators
5. CLI displays formatted list to user

**Update Task Flow**:
1. User enters task ID and new data via menu
2. CLI validates ID is numeric (catch ValueError)
3. CLI calls `TaskManager.update_task(id, title?, description?)`
4. TaskManager checks if ID exists (raise `TaskNotFoundError` if not)
5. TaskManager validates provided data (if any)
6. TaskManager updates Task attributes
7. TaskManager returns updated Task to CLI
8. CLI formats and displays confirmation

### Error Handling Strategy

**CLI Layer**:
- Catch `ValueError` from non-numeric ID input
- Display user-friendly error: "Invalid input. Please enter a numeric task ID."
- Never let exceptions crash application

**Logic Layer**:
- Raise `TaskNotFoundError` for invalid task IDs
- Raise `InvalidTaskDataError` for empty/invalid data
- Never modify state if validation fails

**User Experience**:
- All errors have clear, actionable messages
- User can retry operation without restarting
- No stack traces shown to user

## Quality Gates

All code must pass these gates before being considered complete:

### 1. Type Checking

```bash
mypy src/todo_cli
```

**Expected**: Success with no errors

**Configuration**: `mypy.ini` with strict mode
- Disallow untyped definitions
- Disallow any generics
- Warn on return any

### 2. Linting

```bash
ruff check src/todo_cli
```

**Expected**: All checks passed

**Configuration**: `pyproject.toml`
- Line length: 100
- Target Python: 3.13
- Select: E (errors), F (pyflakes), W (warnings), I (import sorting), N (naming), UP (pyupgrade)

### 3. Tests

```bash
pytest
```

**Expected**: 100% test pass rate

**Coverage**: Minimum 80% for core logic (TaskManager)

### 4. Format Check

```bash
ruff format --check src/todo_cli
```

**Expected**: All files formatted correctly

## Next Steps

### Immediate Next Actions

1. **Create project structure** (follow `quickstart.md`)
   - Run `uv init todo-cli`
   - Create directories per plan
   - Install dev dependencies

2. **Implement Task entity** (TDD)
   - Write failing tests in `tests/unit/test_task_model.py`
   - Implement `src/todo_cli/models/task.py`
   - Run tests, ensure green

3. **Implement TaskManager** (TDD)
   - Write failing tests in `tests/unit/test_task_manager.py`
   - Implement `src/todo_cli/core/task_manager.py`
   - Implement `src/todo_cli/core/exceptions.py`
   - Run tests, ensure green

4. **Implement CLI layer**
   - Write tests in `tests/integration/test_cli_flows.py`
   - Implement `src/todo_cli/cli/formatter.py`
   - Implement `src/todo_cli/cli/interface.py`
   - Create `src/todo_cli/__main__.py`
   - Run tests, ensure green

5. **Quality Gates**
   - Run `mypy src/todo_cli`
   - Run `ruff check src/todo_cli && ruff format src/todo_cli`
   - Run `pytest --cov=src/todo_cli`
   - Fix any failures

### Follow-up Actions

- Run `/sp.tasks` to generate testable task breakdown
- Review architecture decision record (if needed)
- Begin implementation following TDD cycle

## Open Questions

**None** - All research completed, all decisions documented, all gates validated.

## Risks & Mitigations

### Risk 1: Data Loss Confusion

**Mitigation**:
- Display warning on startup: "Note: Tasks are stored in memory only and will be lost when you exit."
- Include reminder in Exit confirmation prompt

### Risk 2: Input Validation Gaps

**Mitigation**:
- Comprehensive test coverage for edge cases
- Never allow unhandled exceptions to crash application
- Clear error messages guide users to correct input

### Risk 3: CLI Usability

**Mitigation**:
- Clear, formatted output using formatter module
- Consistent menu structure
- Helpful prompts and error messages

## Appendix: Quick Reference

### File Locations

| Component | Path | Purpose |
|-----------|------|----------|
| Task entity | `src/todo_cli/models/task.py` | Data class for todo item |
| TaskManager | `src/todo_cli/core/task_manager.py` | CRUD operations |
| Exceptions | `src/todo_cli/core/exceptions.py` | Custom error hierarchy |
| Formatter | `src/todo_cli/cli/formatter.py` | Output formatting helpers |
| Interface | `src/todo_cli/cli/interface.py` | Menu and user interaction |
| Entry Point | `src/todo_cli/__main__.py` | Main application loop |

### Key Methods

| Component | Method | Signature | Purpose |
|-----------|--------|-----------|---------|
| TaskManager | `add_task()` | `add_task(title: str, description: str) -> Task` | Create new task |
| TaskManager | `view_tasks()` | `view_tasks() -> List[Task]` | List all tasks |
| TaskManager | `get_task()` | `get_task(task_id: int) -> Task` | Retrieve single task |
| TaskManager | `update_task()` | `update_task(task_id: int, title: str | None, description: str | None) -> Task` | Modify task |
| TaskManager | `delete_task()` | `delete_task(task_id: int) -> None` | Remove task |
| TaskManager | `toggle_status()` | `toggle_status(task_id: int) -> Task` | Flip completion |

### Status Indicators

| State | Symbol | Display |
|-------|---------|----------|
| Pending | `[ ]` | `[ 1] [ ] Buy groceries: Milk, bread` |
| Complete | `[x]` | `[ 2] [x] Call dentist: Schedule checkup` |

---

**Document Status**: ✅ COMPLETE
**Next Phase**: Run `/sp.tasks` to generate implementation task breakdown
