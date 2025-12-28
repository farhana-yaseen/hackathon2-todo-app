"""
Integration tests for CLI user flows.

These tests cover end-to-end user scenarios across the entire application,
validating that user stories work as expected when all components interact.
"""

import pytest

from todo_cli.core.task_manager import TaskManager
from todo_cli.cli.formatter import TaskFormatter


class TestAddAndViewTasksFlow:
    """Integration test for add task and view tasks flow (User Story 1)."""

    def test_add_task_and_view_in_list(self) -> None:
        """Add task then view list to verify it appears with correct display."""
        # This will fail until full implementation is complete
        # Integration test validates:
        # 1. Add task operation succeeds
        # 2. Task appears in view list
        # 3. Task shows correct status indicator `[ ]`
        # 4. Task displays ID, title, and description
        pass


class TestViewTasksEmptyList:
    """Integration test for viewing tasks when list is empty (User Story 1)."""

    def test_view_tasks_with_no_tasks_shows_friendly_message(self) -> None:
        """Viewing tasks with no tasks displays a friendly message."""
        manager = TaskManager()
        tasks = manager.view_tasks()
        output = TaskFormatter.format_task_list(tasks)
        assert "No tasks yet" in output


class TestToggleCompleteFlow:
    """Integration test for toggle complete flow (User Story 2)."""

    def test_toggle_task_status_and_verify_display(self) -> None:
        """Add task, toggle status, view list to verify change."""
        manager = TaskManager()
        task = manager.add_task("Test Task", "Description")

        # Initially pending
        assert task.is_complete is False

        # Toggle to complete
        updated = manager.toggle_status(task.id)
        assert updated.is_complete is True

        # View in list
        tasks = manager.view_tasks()
        output = TaskFormatter.format_task_list(tasks)
        assert "[x]" in output

        # Toggle back to pending
        updated = manager.toggle_status(task.id)
        assert updated.is_complete is False


class TestUpdateTaskFlow:
    """Integration test for update task flow (User Story 3)."""

    def test_update_task_title_and_verify_in_list(self) -> None:
        """Create task, update title, verify change in list."""
        manager = TaskManager()
        task = manager.add_task("Original Title", "Description")

        # Update title
        updated = manager.update_task(task.id, "Updated Title", None)
        assert updated.title == "Updated Title"
        assert updated.description == "Description"

        # Verify in list
        tasks = manager.view_tasks()
        assert "Updated Title" in TaskFormatter.format_task_list(tasks)

    def test_update_task_description_and_verify_in_list(self) -> None:
        """Create task, update description, verify change in list."""
        manager = TaskManager()
        task = manager.add_task("Title", "Original Description")

        # Update description
        updated = manager.update_task(task.id, None, "Updated Description")
        assert updated.title == "Title"
        assert updated.description == "Updated Description"

        # Verify in list
        tasks = manager.view_tasks()
        assert "Updated Description" in TaskFormatter.format_task_list(tasks)


class TestDeleteTaskFlow:
    """Integration test for delete task flow (User Story 4)."""

    def test_delete_task_and_verify_removed_from_list(self) -> None:
        """Create tasks, delete one, verify removal."""
        manager = TaskManager()
        task1 = manager.add_task("Task 1", "Description 1")
        task2 = manager.add_task("Task 2", "Description 2")
        task3 = manager.add_task("Task 3", "Description 3")

        # Verify 3 tasks
        assert len(manager.view_tasks()) == 3

        # Delete task2
        manager.delete_task(task2.id)

        # Verify 2 tasks remain
        tasks = manager.view_tasks()
        assert len(tasks) == 2

        # Verify IDs not reused
        task_ids = [task.id for task in tasks]
        assert task2.id not in task_ids
        assert 1 in task_ids
        assert 3 in task_ids
