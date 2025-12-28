# Data Model: Todo CLI (Phase I)

**Feature**: 001-todo-cli
**Created**: 2025-12-28
**Status**: Final

## Overview

This document defines the data entities, relationships, validation rules, and state transitions for the Todo CLI application. The model focuses on a single entity (Task) with simple in-memory storage.

## Entity: Task

### Purpose
Represents a single todo item with title, description, and completion status.

### Attributes

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | `int` | Yes | Auto-generated | Positive integer, unique within session | Unique identifier for the task |
| `title` | `str` | Yes | None | Non-empty, non-whitespace, max 200 chars | Short name of the task |
| `description` | `str` | Yes | None | Non-empty, non-whitespace, max 1000 chars | Detailed explanation of the task |
| `is_complete` | `bool` | Yes | `False` | Boolean value | Completion status (True = complete, False = pending) |

### Validation Rules

#### Title Validation
- **Rule**: Must be non-empty after stripping whitespace
- **Error**: `InvalidTaskDataError("Title cannot be empty")`
- **Examples**:
  - Valid: `"Buy groceries"`, `"  Call mom  "` (trimmed to `"Call mom"`)
  - Invalid: `""`, `"   "`, `"\n\t"`

#### Description Validation
- **Rule**: Must be non-empty after stripping whitespace
- **Error**: `InvalidTaskDataError("Description cannot be empty")`
- **Examples**:
  - Valid: `"Get milk and bread"`, `"  Important task  "`
  - Invalid: `""`, `"     "`, `"\n"`

#### ID Validation (for operations)
- **Rule**: Must exist in current task storage
- **Error**: `TaskNotFoundError(f"Task #{task_id} not found")`
- **Examples**:
  - Valid: ID exists in `_tasks` dict
  - Invalid: ID not present in `_tasks` dict

### State Machine

Tasks have a simple binary state:

```
┌─────────┐  toggle_status()  ┌──────────┐
│ Pending ├──────────────────>│ Complete │
│ [ ]     │                    │ [x]      │
└─────────┘<──────────────────┤          │
            toggle_status()     └──────────┘
```

**States**:
- **Pending**: `is_complete = False`, Display: `[ ]`
- **Complete**: `is_complete = True`, Display: `[x]`

**Transitions**:
- `toggle_status()`: Flips `is_complete` boolean (no conditional logic)

**Invariants**:
- A task always has exactly one state (Pending or Complete)
- State transitions always succeed if task ID exists
- No other attributes change during state transition

### Python Implementation

```python
from dataclasses import dataclass

@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique identifier (auto-generated, sequential)
        title: Short name of the task (non-empty string)
        description: Detailed explanation (non-empty string)
        is_complete: Completion status (default: False)
    """
    id: int
    title: str
    description: str
    is_complete: bool = False

    def __post_init__(self) -> None:
        """Validate task data after initialization."""
        if not self.title or not self.title.strip():
            raise InvalidTaskDataError("Title cannot be empty")
        if not self.description or not self.description.strip():
            raise InvalidTaskDataError("Description cannot be empty")

        # Normalize: strip whitespace from title and description
        self.title = self.title.strip()
        self.description = self.description.strip()
```

### Display Format

Tasks are displayed in the CLI using this format:

```
[{id}] [{status}] {title}: {description}
```

**Examples**:
- Pending task: `[1] [ ] Buy groceries: Milk, bread, eggs`
- Complete task: `[2] [x] Call dentist: Schedule annual checkup`

**Formatting Rules**:
- ID: Left-padded to 3 digits for alignment (e.g., `[  1]`, `[ 12]`, `[123]`)
- Status: Fixed width 3 chars including brackets (`[ ]` or `[x]`)
- Title: Truncated to 30 chars with `...` if longer
- Description: Wrapped at 50 chars for readability

## Storage Model

### Structure

```python
class TaskManager:
    """
    Manages in-memory task storage and operations.

    Attributes:
        _tasks: Dictionary mapping task ID to Task instance
        _next_id: Counter for generating sequential IDs
    """
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
```

### Storage Operations

| Operation | Method | Time Complexity | Description |
|-----------|--------|-----------------|-------------|
| Create | `add_task()` | O(1) | Insert task into dict with auto-generated ID |
| Read (single) | `get_task(id)` | O(1) | Retrieve task by ID from dict |
| Read (all) | `view_tasks()` | O(n) | Iterate over all tasks in dict |
| Update | `update_task(id, ...)` | O(1) | Modify task fields by ID |
| Delete | `delete_task(id)` | O(1) | Remove task from dict by ID |
| Toggle | `toggle_status(id)` | O(1) | Flip is_complete boolean |

### ID Generation

```python
def _generate_id(self) -> int:
    """
    Generate next sequential task ID.

    Returns:
        int: Next available task ID
    """
    task_id = self._next_id
    self._next_id += 1
    return task_id
```

**Properties**:
- IDs start at 1
- IDs increment sequentially (1, 2, 3, ...)
- IDs are never reused within a session
- ID counter continues even after deletions (e.g., delete task 2 → next task is still 4, not 2)

### Storage Invariants

1. **Unique IDs**: No two tasks can have the same ID
2. **Sequential IDs**: IDs increase monotonically
3. **No Gaps on Creation**: Tasks are added with consecutive IDs (gaps only from deletion)
4. **All Tasks Valid**: Every task in storage passes validation rules

## Relationships

**No relationships in Phase I** - Tasks are independent entities with no parent/child, category, or tag associations.

## Data Lifecycle

### Task Creation
1. User provides title and description via CLI
2. CLI passes to `TaskManager.add_task(title, description)`
3. TaskManager validates inputs (non-empty strings)
4. TaskManager generates next ID
5. TaskManager creates Task instance
6. TaskManager stores in `_tasks` dict
7. TaskManager returns Task instance to CLI
8. CLI displays confirmation message

### Task Modification
1. User provides task ID and new data via CLI
2. CLI passes to `TaskManager.update_task(id, title?, description?)`
3. TaskManager validates ID exists
4. TaskManager validates new data (if provided)
5. TaskManager updates task attributes
6. TaskManager returns updated Task to CLI
7. CLI displays confirmation message

### Task Deletion
1. User provides task ID via CLI
2. CLI passes to `TaskManager.delete_task(id)`
3. TaskManager validates ID exists
4. TaskManager removes task from `_tasks` dict
5. TaskManager returns success to CLI
6. CLI displays confirmation message

**Note**: Deleted task IDs are never reused. ID counter continues from highest value.

### Session Lifecycle
- **Startup**: TaskManager initialized with empty `_tasks` dict, `_next_id = 1`
- **Runtime**: Tasks added, modified, deleted in memory
- **Shutdown**: All task data discarded (in-memory only)

**No persistence** - data is lost when application exits.

## Error Handling

### Exception Hierarchy

```python
class TodoError(Exception):
    """Base exception for todo CLI."""
    pass

class TaskNotFoundError(TodoError):
    """Raised when task ID doesn't exist."""
    def __init__(self, task_id: int):
        super().__init__(f"Task #{task_id} not found")
        self.task_id = task_id

class InvalidTaskDataError(TodoError):
    """Raised when task data fails validation."""
    pass
```

### Error Scenarios

| Scenario | Exception | Handling |
|----------|-----------|----------|
| Add task with empty title | `InvalidTaskDataError` | CLI displays error, prompts retry |
| Add task with whitespace-only description | `InvalidTaskDataError` | CLI displays error, prompts retry |
| Update non-existent task ID | `TaskNotFoundError` | CLI displays "Task #X not found" |
| Delete non-existent task ID | `TaskNotFoundError` | CLI displays "Task #X not found" |
| Toggle non-existent task ID | `TaskNotFoundError` | CLI displays "Task #X not found" |
| Non-numeric ID input | `ValueError` | CLI catches, displays "Invalid input. Please enter a numeric task ID." |

## Testing Strategy

### Unit Tests for Task Entity

```python
# tests/unit/test_task_model.py

def test_task_creation_valid():
    """Task created with valid data."""
    task = Task(id=1, title="Test", description="Test description")
    assert task.id == 1
    assert task.title == "Test"
    assert task.is_complete is False

def test_task_creation_empty_title():
    """Task creation fails with empty title."""
    with pytest.raises(InvalidTaskDataError, match="Title cannot be empty"):
        Task(id=1, title="", description="Valid description")

def test_task_creation_whitespace_description():
    """Task creation fails with whitespace-only description."""
    with pytest.raises(InvalidTaskDataError, match="Description cannot be empty"):
        Task(id=1, title="Valid", description="   ")

def test_task_strips_whitespace():
    """Task strips leading/trailing whitespace."""
    task = Task(id=1, title="  Title  ", description="  Desc  ")
    assert task.title == "Title"
    assert task.description == "Desc"
```

### Unit Tests for TaskManager Storage

```python
# tests/unit/test_task_manager.py

def test_add_task_generates_sequential_ids():
    """IDs increment sequentially."""
    manager = TaskManager()
    task1 = manager.add_task("First", "Description 1")
    task2 = manager.add_task("Second", "Description 2")
    assert task1.id == 1
    assert task2.id == 2

def test_get_task_not_found():
    """Getting non-existent task raises exception."""
    manager = TaskManager()
    with pytest.raises(TaskNotFoundError):
        manager.get_task(999)

def test_delete_task_removes_from_storage():
    """Deleted task no longer retrievable."""
    manager = TaskManager()
    task = manager.add_task("Test", "Description")
    manager.delete_task(task.id)
    with pytest.raises(TaskNotFoundError):
        manager.get_task(task.id)

def test_ids_not_reused_after_deletion():
    """IDs continue incrementing after deletion."""
    manager = TaskManager()
    task1 = manager.add_task("First", "Desc")
    task2 = manager.add_task("Second", "Desc")
    manager.delete_task(task1.id)
    task3 = manager.add_task("Third", "Desc")
    assert task3.id == 3  # Not 1 (reused)
```

## Migration Path (Future Phases)

**Phase I**: In-memory Dict[int, Task]

**Phase II** (hypothetical):
- Add file persistence (JSON/CSV)
- Same data model, add serialization/deserialization
- Maintain backward compatibility (same Task attributes)

**Phase III** (hypothetical):
- Add database persistence (SQLite)
- Same data model, add ORM mapping
- Introduce migrations for schema changes

**Data model remains stable** - architectural changes don't affect Task entity definition.

## Summary

**Single Entity**: Task (id, title, description, is_complete)
**Storage**: Dict[int, Task] with sequential ID generation
**Validation**: Non-empty title/description, existing task ID for operations
**State**: Binary (Pending/Complete) with toggle transition
**Lifecycle**: Created → (Updated, Toggled)* → Deleted
**Persistence**: None (in-memory only for Phase I)

All design decisions align with constitution principles:
- Simple data model (YAGNI)
- Clear validation rules (Error Handling principle)
- Testable entities (Test-First principle)
- Type-annotated (Type Hinting principle)
