"""
Task entity representing a single todo item.

This module defines the Task dataclass with validation rules
as specified in the project data model.
"""

from dataclasses import dataclass

from todo_cli.core.exceptions import InvalidTaskDataError


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique identifier (auto-generated, sequential)
        title: Short name of task (non-empty string)
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
