"""
Custom exception hierarchy for todo CLI application.

All domain-specific exceptions inherit from TodoError base class.
"""


class TodoError(Exception):
    """Base exception for todo CLI application."""
    pass


class TaskNotFoundError(TodoError):
    """Raised when a task ID doesn't exist in the task storage."""

    def __init__(self, task_id: int):
        super().__init__(f"Task #{task_id} not found")
        self.task_id = task_id


class InvalidTaskDataError(TodoError):
    """Raised when task data fails validation."""

    pass
