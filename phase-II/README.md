# Todo CLI

A simple in-memory command-line todo application written in Python.

## Features

- Create tasks with titles and descriptions
- View all tasks with status indicators
- Mark tasks as complete/pending
- Update task titles and descriptions
- Delete tasks
- **Important**: Tasks are stored in memory only - they will be lost when you exit!

## Installation

```bash
# Install dependencies
pip install -e .
```

## Usage

Run the application:

```bash
todo-cli
```

You'll see a menu of options:

```
--- TODO APPLICATION ---
1. View Tasks
2. Add Task
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit
```

### 1. View Tasks

Shows all tasks with their ID, status, title, and description.

Status indicators:
- `[ ]` - Pending task
- `[x]` - Complete task

Example output:
```
[   1] [ ] Buy groceries
    Description: Milk, bread, eggs
```

### 2. Add Task

Create a new task.

Example:
```
Title: Buy groceries
Description: Milk, bread, eggs
```

### 3. Update Task

Update an existing task's title and/or description.

Example:
```
Enter task ID to update: 1
New title (press Enter to keep current):
New description (press Enter to keep current): Milk, bread, eggs, butter
```

### 4. Delete Task

Remove a task by ID.

Example:
```
Enter task ID to delete: 1
```

### 5. Toggle Complete

Mark a task as complete or pending.

Example:
```
Enter task ID to toggle: 1
```

### 6. Exit

Exit the application with a confirmation prompt.

## Important Notes

### Data Loss Warning

**This application stores all tasks in memory only.**

When you exit the application, all tasks will be permanently lost.

This is by design - it's a simple, lightweight todo CLI for temporary task tracking during a single session.

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/todo_cli --cov-report=term-missing
```

### Type Checking

```bash
# Run mypy type checking
cd src && python -m mypy todo_cli --explicit-package-bases
```

### Linting

```bash
# Run ruff
ruff check src/todo_cli

# Format code
ruff format src/todo_cli
```

## Project Structure

```
src/todo_cli/
  models/task.py          - Task dataclass with validation
  core/
    exceptions.py        - Custom exception hierarchy
    task_manager.py     - Business logic layer
  cli/
    formatter.py        - Output formatting
    interface.py        - Menu-driven CLI interface
  __main__.py         - Application entry point
```

## Tech Stack

- Python 3.13+
- pytest - Testing
- mypy - Type checking
- ruff - Linting and formatting
