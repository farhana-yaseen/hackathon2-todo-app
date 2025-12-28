# Research & Technical Decisions: Todo CLI (Phase I)

**Feature**: 001-todo-cli
**Created**: 2025-12-28
**Status**: Complete

## Overview

This document captures research findings and technical decisions for implementing the In-Memory Todo CLI Application. All decisions align with the project constitution and focus on simplicity, testability, and clean code principles.

## Research Topics

### 1. Python 3.13+ Project Setup with uv

**Decision**: Use uv for dependency management and virtual environment

**Rationale**:
- uv is explicitly required in constitution (Mandatory Technologies)
- Faster than pip/poetry for dependency resolution
- Modern Python tooling aligned with Python 3.13+
- Simpler project initialization and dependency management

**Setup approach**:
```bash
uv init todo-cli
uv venv
uv pip install pytest mypy ruff
```

**Alternatives considered**:
- **Poetry**: More mature but slower, adds unnecessary complexity for Phase I
- **pip + venv**: Standard library approach but lacks modern dependency resolution
- **Rejected because**: uv is constitution-mandated and provides better developer experience

### 2. Project Structure for CLI Application

**Decision**: Single project structure with clear layer separation

**Rationale**:
- Phase I is a simple, standalone CLI tool (no web/mobile components)
- Constitution mandates separation: CLI Layer → Logic Layer → Data Layer
- Testable design requires logic independent of CLI
- Follows Python best practices for package structure

**Chosen Structure**:
```
src/todo_cli/
├── __init__.py
├── __main__.py           # Entry point (python -m todo_cli)
├── models/
│   ├── __init__.py
│   └── task.py           # Task dataclass (Data Layer)
├── core/
│   ├── __init__.py
│   ├── task_manager.py   # CRUD operations (Logic Layer)
│   └── exceptions.py     # Custom exceptions
└── cli/
    ├── __init__.py
    ├── interface.py      # Menu and user interaction (CLI Layer)
    └── formatter.py      # Output formatting helpers

tests/
├── unit/
│   ├── test_task.py
│   ├── test_task_manager.py
│   └── test_formatter.py
└── integration/
    └── test_cli_flows.py
```

**Alternatives considered**:
- **Flat structure** (all files in src/): Rejected - violates separation of concerns principle
- **Feature-based** (src/add_task/, src/view_tasks/): Rejected - over-engineering for 5 operations
- **Monolithic** (single main.py file): Rejected - untestable, violates constitution principles

### 3. Data Model Implementation

**Decision**: Use Python `@dataclass` for Task entity

**Rationale**:
- Built-in Python 3.7+ feature, no external dependencies
- Automatic `__init__`, `__repr__`, `__eq__` generation
- Immutable option with `frozen=True` for data integrity
- Type hints integrated naturally
- Validates against constitution's type hinting requirement

**Implementation**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    description: str
    is_complete: bool = False
```

**Alternatives considered**:
- **NamedTuple**: Rejected - less flexible, no default values
- **attrs library**: Rejected - external dependency, dataclass sufficient
- **Plain class**: Rejected - boilerplate code, no auto-generated methods

### 4. In-Memory Storage Strategy

**Decision**: Dict[int, Task] in TaskManager class

**Rationale**:
- O(1) lookup by task ID for update/delete/toggle operations
- Constitution permits dictionaries/lists for in-memory storage
- Simple, no need for complex data structures
- Easy to iterate for view operations: `dict.values()`

**Implementation**:
```python
class TaskManager:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
```

**Alternatives considered**:
- **List[Task]**: Rejected - O(n) lookup requires iterating to find task by ID
- **List + separate ID counter**: Rejected - more complex than dict, no benefits
- **OrderedDict**: Rejected - unnecessary, regular dict maintains insertion order in Python 3.7+

### 5. ID Generation Strategy

**Decision**: Sequential integer counter starting from 1

**Rationale**:
- Spec requirement: "sequential integer ID, starting from 1"
- User-friendly (short, memorable IDs like 1, 2, 3)
- No collision risk in single-session in-memory context
- Simple to implement and test

**Implementation**:
```python
def _generate_id(self) -> int:
    task_id = self._next_id
    self._next_id += 1
    return task_id
```

**Alternatives considered**:
- **UUID**: Rejected - overkill for in-memory CLI, not user-friendly (long strings)
- **Hash-based**: Rejected - no benefit, adds complexity
- **ID reuse after deletion**: Rejected - spec explicitly states IDs not reused

### 6. Input Validation Approach

**Decision**: Custom exception hierarchy + validation in TaskManager

**Rationale**:
- Constitution mandates custom exceptions (TaskNotFoundError, InvalidTaskDataError)
- Centralized validation in logic layer, not CLI
- Clear error types for specific failure modes
- Testable validation logic independent of user interface

**Exception Hierarchy**:
```python
class TodoError(Exception):
    """Base exception for todo CLI"""
    pass

class TaskNotFoundError(TodoError):
    """Raised when task ID doesn't exist"""
    pass

class InvalidTaskDataError(TodoError):
    """Raised when task data fails validation"""
    pass
```

**Validation Rules**:
- Title: non-empty, non-whitespace (strip and check length)
- Description: non-empty, non-whitespace (strip and check length)
- Task ID: must exist in `_tasks` dict for update/delete/toggle

**Alternatives considered**:
- **Pydantic**: Rejected - external dependency, overkill for simple validation
- **Return codes (True/False)**: Rejected - doesn't align with exception-based constitution guidance
- **Validation in CLI layer**: Rejected - violates "No Business Logic in UI" principle

### 7. CLI Menu Design Pattern

**Decision**: Loop-based menu with numbered options

**Rationale**:
- Matches spec's example UI layout (numbered menu 1-6)
- Intuitive for users (select number, press Enter)
- Easy to implement and test
- Clear exit condition (option 6 or specific input)

**Menu Flow**:
1. Display menu
2. Get user input
3. Parse input (validate numeric)
4. Dispatch to appropriate handler method
5. Display result/error
6. Return to menu (unless exit selected)

**Alternatives considered**:
- **Argument-based CLI** (like `git` commands): Rejected - spec requires interactive menu
- **readline with autocomplete**: Rejected - over-engineering, adds dependency
- **TUI framework** (like `rich` or `textual`): Rejected - external dependency, unnecessary complexity

### 8. Testing Strategy

**Decision**: pytest with unit + integration tests

**Rationale**:
- Constitution mandates pytest as testing framework
- Unit tests: Test TaskManager and Task independently (fast, isolated)
- Integration tests: Test full CLI flows end-to-end (user scenarios)
- Use pytest fixtures for common test data and TaskManager instances

**Test Coverage Targets**:
- **Unit Tests**:
  - All TaskManager CRUD methods (add, get, update, delete, toggle)
  - Edge cases: empty strings, non-existent IDs, whitespace-only input
  - Exception raising for validation failures

- **Integration Tests**:
  - User Story 1: Add and view tasks
  - User Story 2: Toggle completion status
  - User Story 3: Update task details
  - User Story 4: Delete tasks
  - Edge cases: non-numeric input, empty list display

**Test Organization**:
```
tests/
├── unit/
│   ├── test_task_model.py         # Task dataclass tests
│   ├── test_task_manager_add.py   # Add task tests
│   ├── test_task_manager_update.py
│   ├── test_task_manager_delete.py
│   ├── test_task_manager_toggle.py
│   └── test_task_manager_view.py
└── integration/
    └── test_cli_user_flows.py     # End-to-end scenarios
```

**Alternatives considered**:
- **unittest**: Rejected - pytest is constitution-mandated
- **Only integration tests**: Rejected - violates TDD principle, slow feedback
- **Only unit tests**: Rejected - doesn't verify user scenarios work end-to-end

### 9. Type Checking Configuration

**Decision**: mypy with strict mode

**Rationale**:
- Constitution mandates mypy for type checking
- Strict mode enforces "mandatory type hints for all functions/methods"
- Catches type errors before runtime
- Aligns with "Type Hinting: Mandatory" principle

**mypy.ini Configuration**:
```ini
[mypy]
python_version = 3.13
strict = True
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_generics = True
```

**Alternatives considered**:
- **Pyright**: Rejected - mypy is constitution-mandated
- **Non-strict mypy**: Rejected - doesn't enforce mandatory type hints
- **No type checking**: Rejected - violates constitution

### 10. Code Quality Tools Configuration

**Decision**: ruff for linting (PEP 8 compliance)

**Rationale**:
- Constitution permits "ruff or flake8", ruff is faster
- Single tool for linting + auto-formatting
- Catches PEP 8 violations, unused imports, code smells
- Fast enough to run on every save/commit

**pyproject.toml Configuration**:
```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP"]
ignore = []

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__
```

**Alternatives considered**:
- **flake8**: Slower than ruff, constitution allows choice
- **black**: Ruff can handle both linting and formatting
- **No linting**: Rejected - violates "PEP 8 Compliance: Strict" principle

## Technical Constraints Validation

### Constraints from Spec

| Constraint | Implementation Approach | Validation |
|------------|------------------------|------------|
| Python 3.13+ | Use latest Python features (match statements, type hints) | ✓ Compatible |
| uv package manager | Project setup with `uv init`, dependencies via `uv pip install` | ✓ Constitution-mandated |
| In-memory storage only | Dict[int, Task] in TaskManager, no file I/O | ✓ No persistence layer |
| CLI interface only | No web/GUI frameworks, stdout/stdin only | ✓ Console-based |
| Type hints mandatory | All functions/methods/classes have full type annotations | ✓ Enforced by mypy strict |
| Menu-driven interface | Numbered menu with continuous loop | ✓ Matches spec example |

### Constitution Validation

| Principle | How Addressed | Status |
|-----------|---------------|--------|
| Clean Code & Maintainability | PEP 8 (ruff), type hints (mypy), clear naming | ✓ Gates in place |
| Architecture & Separation | 3 layers (CLI/Logic/Data), testable design | ✓ Structure defined |
| Test-First Development | pytest, unit + integration, TDD workflow | ✓ Test strategy documented |
| Error Handling & Validation | Custom exceptions, input validation in logic layer | ✓ Exception hierarchy planned |
| User Experience | Clear prompts, status indicators, confirmation messages | ✓ Formatter module planned |
| Simplicity & YAGNI | No external dependencies beyond tools, 5 operations only | ✓ No over-engineering |

## Performance Considerations

**Expected Performance** (Phase I):
- **Task operations**: O(1) for add/get/update/delete (dict-based)
- **View all tasks**: O(n) iteration (acceptable for 50 task target)
- **Startup time**: <100ms (no I/O, simple imports)
- **Memory usage**: ~1KB per task × 50 tasks = ~50KB negligible

**No performance concerns for Phase I scope** - in-memory operations are instant for 50 tasks.

## Security Considerations

**Threats**: None significant for Phase I
- No network exposure (local CLI)
- No persistence (no file injection risks)
- No authentication/authorization (single user)
- No sensitive data (todo tasks)

**Input validation** prevents crashes but no security implications beyond stability.

## Dependencies Summary

**Development Dependencies** (via uv):
```
pytest==8.0+        # Testing framework (constitution-mandated)
mypy==1.8+          # Type checking (constitution-mandated)
ruff==0.2+          # Linting (constitution-mandated)
pytest-cov          # Code coverage reporting
```

**Runtime Dependencies**:
- Python 3.13+ standard library only (no external packages)

**Rationale for minimal dependencies**:
- Constitution states "Minimal external dependencies. Prefer standard library"
- Dataclasses, typing, sys, os are all built-in
- CLI doesn't need argparse (interactive menu), readline (simple input), or rich (formatted output not required)

## Open Questions & Risks

### Resolved Questions
- ✓ ID generation strategy: Sequential integers
- ✓ Storage structure: Dict[int, Task]
- ✓ Validation approach: Custom exceptions in logic layer
- ✓ Testing approach: pytest with unit + integration split
- ✓ Project structure: Single project, 3-layer separation

### Remaining Risks

**Risk 1: User confusion about data loss**
- **Mitigation**: Display warning on startup and exit
- **Implementation**: Add startup banner in CLI interface

**Risk 2: Input validation gaps**
- **Mitigation**: Comprehensive test coverage for edge cases
- **Implementation**: Dedicated test files for each validation rule

**Risk 3: CLI usability on Windows/Linux differences**
- **Mitigation**: Use platform-agnostic Python input/print
- **Implementation**: Avoid OS-specific commands, test on multiple platforms

## Next Steps

Phase 0 research complete. Proceed to Phase 1:
1. Create data-model.md with Task entity details
2. Generate contracts/ (N/A for CLI - no API contracts)
3. Create quickstart.md with setup instructions
4. Update agent context with technology choices

All technical decisions validated against constitution and spec requirements.
