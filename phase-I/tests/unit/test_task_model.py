"""
Unit tests for Task dataclass.

Tests follow TDD approach - written first to ensure they fail,
then implementation makes them pass.
"""

import pytest

from todo_cli.models.task import Task
from todo_cli.core.exceptions import InvalidTaskDataError


class TestTaskCreation:
    """Test cases for creating valid Task instances."""

    def test_task_creation_valid(self) -> None:
        """Task created with valid data."""
        task = Task(id=1, title="Buy groceries", description="Test description")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Test description"
        assert task.is_complete is False

    def test_task_complete_by_default(self) -> None:
        """Task is_complete defaults to False."""
        task = Task(id=1, title="Test", description="Description")
        assert task.is_complete is False

    def test_task_complete_can_be_set(self) -> None:
        """Task is_complete can be explicitly set to True."""
        task = Task(id=1, title="Test", description="Description", is_complete=True)
        assert task.is_complete is True


class TestTaskValidation:
    """Test cases for task data validation."""

    def test_task_creation_empty_title_raises_error(self) -> None:
        """Task creation fails with empty title."""
        with pytest.raises(InvalidTaskDataError, match="Title cannot be empty"):
            Task(id=1, title="", description="Valid description")

    def test_task_creation_whitespace_only_title_raises_error(self) -> None:
        """Task creation fails with whitespace-only title."""
        with pytest.raises(InvalidTaskDataError, match="Title cannot be empty"):
            Task(id=1, title="   ", description="Valid description")

    def test_task_creation_newline_title_raises_error(self) -> None:
        """Task creation fails with newline-only title."""
        with pytest.raises(InvalidTaskDataError, match="Title cannot be empty"):
            Task(id=1, title="\n\t", description="Valid description")

    def test_task_creation_empty_description_raises_error(self) -> None:
        """Task creation fails with empty description."""
        with pytest.raises(InvalidTaskDataError, match="Description cannot be empty"):
            Task(id=1, title="Valid title", description="")

    def test_task_creation_whitespace_only_description_raises_error(self) -> None:
        """Task creation fails with whitespace-only description."""
        with pytest.raises(InvalidTaskDataError, match="Description cannot be empty"):
            Task(id=1, title="Valid title", description="     ")

    def test_task_strips_whitespace_from_title(self) -> None:
        """Task strips leading and trailing whitespace from title."""
        task = Task(id=1, title="  Valid Title  ", description="Description")
        assert task.title == "Valid Title"

    def test_task_strips_whitespace_from_description(self) -> None:
        """Task strips leading and trailing whitespace from description."""
        task = Task(id=1, title="Title", description="  Valid Description  ")
        assert task.description == "Valid Description"

    def test_task_trims_internal_whitespace(self) -> None:
        """Task trims whitespace from both title and description."""
        task = Task(id=1, title="  Title  ", description="  Description  ")
        assert task.title == "Title"
        assert task.description == "Description"
