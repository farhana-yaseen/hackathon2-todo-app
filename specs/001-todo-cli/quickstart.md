# Quick Start Guide: Todo CLI (Phase I)

**Feature**: 001-todo-cli
**Created**: 2025-12-28
**Audience**: Developers setting up the project for the first time

## Prerequisites

Before starting, ensure you have:

- **Python 3.13+** installed ([download](https://www.python.org/downloads/))
- **uv** package manager installed ([installation guide](https://github.com/astral-sh/uv))
- **Git** (optional, for version control)

Verify installations:
```bash
python --version  # Should show 3.13.0 or higher
uv --version      # Should show uv version
```

## Project Setup

### 1. Initialize Project with uv

```bash
# Navigate to your workspace
cd ~/projects

# Initialize new Python project
uv init todo-cli
cd todo-cli

# Create virtual environment
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Development Dependencies

```bash
# Install testing, type checking, and linting tools
uv pip install pytest pytest-cov mypy ruff
```

### 3. Create Project Structure

```bash
# Create source directories
mkdir -p src/todo_cli/models
mkdir -p src/todo_cli/core
mkdir -p src/todo_cli/cli

# Create test directories
mkdir -p tests/unit
mkdir -p tests/integration

# Create __init__.py files
touch src/todo_cli/__init__.py
touch src/todo_cli/models/__init__.py
touch src/todo_cli/core/__init__.py
touch src/todo_cli/cli/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

Your structure should look like:
```
todo-cli/
├── src/
│   └── todo_cli/
│       ├── __init__.py
│       ├── __main__.py          # To be created
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py          # To be created
│       ├── core/
│       │   ├── __init__.py
│       │   ├── exceptions.py    # To be created
│       │   └── task_manager.py  # To be created
│       └── cli/
│           ├── __init__.py
│           ├── formatter.py     # To be created
│           └── interface.py     # To be created
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       └── __init__.py
├── pyproject.toml               # To be created
├── mypy.ini                     # To be created
└── README.md                    # To be created
```

### 4. Configure Project Tools

Create `pyproject.toml` in project root:

```toml
[project]
name = "todo-cli"
version = "0.1.0"
description = "In-memory CLI todo application"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "mypy>=1.8",
    "ruff>=0.2",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM"]
ignore = []

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v --cov=src/todo_cli --cov-report=term-missing"

[tool.coverage.run]
source = ["src/todo_cli"]
omit = ["tests/*", "**/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

Create `mypy.ini` in project root:

```ini
[mypy]
python_version = 3.13
strict = True
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_generics = True
warn_redundant_casts = True
warn_unused_ignores = True
no_implicit_optional = True
check_untyped_defs = True

[mypy-tests.*]
disallow_untyped_defs = False
```

## Development Workflow

### Test-Driven Development (TDD) Cycle

The constitution mandates TDD. Follow this workflow:

1. **Write a failing test** (Red)
   ```bash
   # Example: Create test_task.py
   cd tests/unit
   # Write test that will fail
   pytest test_task.py  # Should fail
   ```

2. **Write minimal code to pass test** (Green)
   ```bash
   # Example: Create task.py
   cd src/todo_cli/models
   # Implement just enough to pass
   pytest tests/unit/test_task.py  # Should pass
   ```

3. **Refactor while keeping tests green**
   ```bash
   # Improve code quality
   pytest  # All tests should still pass
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/todo_cli --cov-report=html

# Run specific test file
pytest tests/unit/test_task.py

# Run tests matching pattern
pytest -k "test_add_task"

# Run with verbose output
pytest -v
```

### Type Checking

```bash
# Check all files
mypy src/todo_cli

# Check specific file
mypy src/todo_cli/models/task.py

# Check with verbose output
mypy --show-error-codes src/todo_cli
```

### Linting

```bash
# Check for issues
ruff check src/todo_cli

# Fix auto-fixable issues
ruff check --fix src/todo_cli

# Format code
ruff format src/todo_cli

# Check and format in one command
ruff check --fix src/todo_cli && ruff format src/todo_cli
```

### Running the Application

Once implemented, run the CLI application:

```bash
# From project root with venv activated
python -m todo_cli

# Or install in editable mode
uv pip install -e .
todo-cli  # If entry point configured
```

## Quality Gates Checklist

Before committing code, ensure all gates pass:

```bash
# 1. Type checking
mypy src/todo_cli
# Expected: Success: no issues found

# 2. Linting
ruff check src/todo_cli
# Expected: All checks passed

# 3. Tests
pytest
# Expected: 100% pass rate

# 4. Coverage
pytest --cov=src/todo_cli --cov-report=term-missing
# Expected: ≥80% coverage for core logic

# 5. Format check
ruff format --check src/todo_cli
# Expected: All files formatted correctly
```

**All gates must pass** before code is considered complete (per constitution).

## Common Commands Reference

```bash
# Setup
uv venv                          # Create virtual environment
source .venv/bin/activate        # Activate (Linux/Mac)
.venv\Scripts\activate           # Activate (Windows)
uv pip install -e ".[dev]"       # Install with dev dependencies

# Testing
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest --cov                     # With coverage
pytest -k "test_name"            # Run specific test

# Quality Checks
mypy src/todo_cli                # Type checking
ruff check src/todo_cli          # Linting
ruff format src/todo_cli         # Formatting

# Running
python -m todo_cli               # Run application
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'todo_cli'`

**Solution**: Ensure you're in project root and virtual environment is activated. Install package in editable mode:
```bash
uv pip install -e .
```

### Issue: `mypy` reports "Cannot find implementation or library stub"

**Solution**: Install type stubs for standard library (if needed):
```bash
uv pip install types-all
```

### Issue: Tests fail with import errors

**Solution**: Add project root to PYTHONPATH or install package:
```bash
# Option 1: Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Option 2: Install in editable mode
uv pip install -e .
```

### Issue: `ruff` not found after installation

**Solution**: Ensure virtual environment is activated:
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

## Next Steps

1. **Read the implementation plan**: Review `specs/001-todo-cli/plan.md` for architecture details
2. **Review data model**: Understand entities in `specs/001-todo-cli/data-model.md`
3. **Start with tests**: Follow TDD - write tests first before implementation
4. **Implement Task entity**: Begin with `src/todo_cli/models/task.py` and corresponding tests
5. **Implement TaskManager**: Build CRUD operations in `src/todo_cli/core/task_manager.py`
6. **Build CLI interface**: Create menu-driven interface in `src/todo_cli/cli/interface.py`

## Additional Resources

- **Constitution**: `.specify/memory/constitution.md` - Project principles and standards
- **Feature Spec**: `specs/001-todo-cli/spec.md` - Requirements and user stories
- **Research Doc**: `specs/001-todo-cli/research.md` - Technical decisions and rationale

---

**Questions or issues?** Refer to the constitution or consult the project spec for clarification.

Happy coding! 🚀
