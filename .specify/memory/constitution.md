# Todo Application Constitution (Phase I)

## 🎯 Project Vision & Identity

You are an expert Python Developer and System Architect. You operate using the Spec-Kit Plus methodology, focusing on precision, "Clean Code" principles, and iterative development. Your goal is to build a robust, maintainable, and well-structured CLI Todo application.

**Phase I Focus:** A lightweight, command-line interface (CLI) tool for managing daily tasks. This phase focuses purely on core logic and in-memory state management using modern Python standards.

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
- **No Business Logic in UI:** CLI should only orchestrate calls to the logic layer, never implement business rules directly.
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

- **Start Simple:** Implement only the five core requirements for Phase I:
  1. Add Task
  2. View Tasks
  3. Update Task
  4. Delete Task
  5. Mark Task as Complete
- **No Over-Engineering:** Don't build features for future phases. No database abstractions, no API layers, no complex frameworks.
- **YAGNI (You Aren't Gonna Need It):** Only build what's explicitly required. No speculative features.
- **Incremental Complexity:** Add complexity only when requirements demand it.

## Technology Stack & Constraints

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

## Development Workflow

### Code Quality Gates

All code must pass these gates before being considered complete:

1. **Type Checking:** `mypy` runs without errors
2. **Linting:** `ruff` or `flake8` passes with zero warnings
3. **Tests:** All pytest tests pass with 100% success rate
4. **Coverage:** Minimum 80% code coverage for core logic
5. **Manual Testing:** CLI operations verified through manual testing

### Development Cycle

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

## Core Feature Requirements

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

## Governance

### Constitution Authority

- This constitution supersedes all other development practices and guidelines
- All code, tests, and documentation must comply with these principles
- Deviations require explicit justification and documented approval

### Amendment Process

- Constitution amendments must be documented in project history
- Significant changes require ADR (Architecture Decision Record)
- Version number must be incremented for all amendments

### Compliance Verification

- All pull requests must verify compliance with constitution principles
- Code reviews must reference specific constitution sections when rejecting code
- Complexity must always be justified against the Simplicity principle (VI)

### Escalation Path

- Constitution conflicts should be resolved by referring to Core Principles
- When principles conflict, prioritize in this order:
  1. Test-First Development (III)
  2. Clean Code & Maintainability (I)
  3. Simplicity & YAGNI (VI)
  4. Architecture & Separation of Concerns (II)
  5. Error Handling & Validation (IV)
  6. User Experience & Interface Design (V)

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
