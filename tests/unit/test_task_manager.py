"""
Unit tests for TaskManager.

Tests follow TDD approach - written first to ensure they fail,
then implementation makes them pass.
"""

import pytest

from todo_cli.models.task import Task
from todo_cli.core.exceptions import TaskNotFoundError
from todo_cli.core.task_manager import TaskManager


class TestTaskManagerAddTask:
    """Test cases for TaskManager.add_task method."""

    def test_add_task_generates_sequential_ids(self) -> None:
        """IDs increment sequentially starting from 1."""
        # This will fail until TaskManager.add_task is implemented
        task1 = Task(id=1, title="First", description="Desc 1")
        task2 = Task(id=2, title="Second", description="Desc 2")
        task3 = Task(id=3, title="Third", description="Desc 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_valid_data(self) -> None:
        """Task created with valid title and description."""
        task = Task(id=1, title="Buy groceries", description="Milk, bread, eggs")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, bread, eggs"


class TestTaskManagerViewTasks:
    """Test cases for TaskManager.view_tasks method."""

    def test_view_tasks_returns_all_tasks(self) -> None:
        """view_tasks returns list of all tasks in storage."""
        # This will fail until TaskManager.view_tasks is implemented
        tasks = [Task(id=i, title=f"Task {i}", description=f"Description {i}") for i in range(1, 4)]
        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[2].title == "Task 3"

    def test_view_tasks_returns_empty_list_when_no_tasks(self) -> None:
        """view_tasks returns empty list when no tasks exist."""
        # This will fail until TaskManager.view_tasks is implemented
        pass


class TestTaskManagerGetTask:
    """Test cases for TaskManager.get_task method."""

    def test_get_task_by_existing_id(self) -> None:
        """get_task returns task when ID exists."""
        # This will fail until TaskManager.get_task is implemented
        task = Task(id=1, title="Test", description="Description")
        assert task.id == 1
        assert task.title == "Test"

    def test_get_task_by_nonexistent_id_raises_error(self) -> None:
        """get_task raises TaskNotFoundError when ID doesn't exist."""
        # This will fail until TaskManager.get_task is implemented
        from todo_cli.core.task_manager import TaskManager
        manager = TaskManager()
        with pytest.raises(TaskNotFoundError, match="Task #999 not found"):
            manager.get_task(999)


class TestTaskManagerUpdateTask:
    """Test cases for TaskManager.update_task method."""

    def test_update_task_title_only(self) -> None:
        """Update task title only."""
        manager = TaskManager()
        manager.add_task("Original", "Description")
        updated = manager.update_task(1, "Updated", None)
        assert updated.title == "Updated"
        assert updated.description == "Description"

    def test_update_task_description_only(self) -> None:
        """Update task description only."""
        manager = TaskManager()
        manager.add_task("Title", "Original Desc")
        updated = manager.update_task(1, None, "New Desc")
        assert updated.title == "Title"
        assert updated.description == "New Desc"

    def test_update_task_both_fields(self) -> None:
        """Update both title and description."""
        manager = TaskManager()
        manager.add_task("Title", "Description")
        updated = manager.update_task(1, "New Title", "New Description")
        assert updated.title == "New Title"
        assert updated.description == "New Description"

    def test_update_task_nonexistent_id_raises_error(self) -> None:
        """Update non-existent task raises TaskNotFoundError."""
        manager = TaskManager()
        manager.add_task("Test", "Description")
        with pytest.raises(TaskNotFoundError, match="Task #999 not found"):
            manager.update_task(999, "New Title", "New Desc")

    def test_update_task_empty_title_raises_error(self) -> None:
        """Update with empty title raises InvalidTaskDataError."""
        from todo_cli.core.exceptions import InvalidTaskDataError
        manager = TaskManager()
        manager.add_task("Test", "Description")
        with pytest.raises(InvalidTaskDataError, match="Title cannot be empty"):
            manager.update_task(1, "", None)


class TestTaskManagerToggleStatus:
    """Test cases for TaskManager.toggle_status method."""

    def test_toggle_pending_to_complete(self) -> None:
        """Toggle pending task to complete."""
        manager = TaskManager()
        manager.add_task("Test", "Description")
        updated = manager.toggle_status(1)
        assert updated.is_complete is True
        assert updated.title == "Test"

    def test_toggle_complete_to_pending(self) -> None:
        """Toggle complete task back to pending."""
        manager = TaskManager()
        task = manager.add_task("Test", "Description")
        task.is_complete = True
        updated = manager.toggle_status(1)
        assert updated.is_complete is False
        assert updated.title == "Test"

    def test_toggle_nonexistent_id_raises_error(self) -> None:
        """Toggle non-existent task raises TaskNotFoundError."""
        manager = TaskManager()
        with pytest.raises(TaskNotFoundError, match="Task #999 not found"):
            manager.toggle_status(999)


class TestTaskManagerDeleteTask:
    """Test cases for TaskManager.delete_task method."""

    def test_delete_task_removes_from_storage(self) -> None:
        """Delete task removes it from storage."""
        manager = TaskManager()
        manager.add_task("Test", "Description")
        manager.delete_task(1)
        with pytest.raises(TaskNotFoundError):
            manager.get_task(1)

    def test_delete_task_nonexistent_id_raises_error(self) -> None:
        """Delete non-existent task raises TaskNotFoundError."""
        manager = TaskManager()
        manager.add_task("Test", "Description")
        with pytest.raises(TaskNotFoundError, match="Task #999 not found"):
            manager.delete_task(999)
