"""
TaskManager handles in-memory task storage and all CRUD operations.

This module provides the logic layer for the todo CLI application,
separating business rules from the CLI interface.
"""


from todo_cli.core.exceptions import InvalidTaskDataError, TaskNotFoundError
from todo_cli.models.task import Task


class TaskManager:
    """
    Manages in-memory task storage and operations.

    Attributes:
        _tasks: Dictionary mapping task ID to Task instance
        _next_id: Counter for generating sequential IDs
    """

    def __init__(self) -> None:
        """Initialize empty task storage with ID counter at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """
        Generate next sequential task ID.

        Returns:
            int: Next available task ID
        """
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def add_task(self, title: str, description: str) -> Task:
        """
        Add a new task to storage.

        Args:
            title: Short name of task (must be non-empty)
            description: Detailed explanation of task (must be non-empty)

        Returns:
            Task: Created task instance with auto-generated ID

        Raises:
            InvalidTaskDataError: If title or description is empty
        """
        task_id = self._generate_id()
        task = Task(id=task_id, title=title, description=description)
        self._tasks[task_id] = task
        return task

    def view_tasks(self) -> list[Task]:
        """
        Return all tasks in storage.

        Returns:
            List[Task]: List of all Task instances in storage order
        """
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task by ID.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Task: Task instance

        Raises:
            TaskNotFoundError: If task ID doesn't exist in storage
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> Task:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: ID of task to update
            title: New title (optional, press Enter to keep current)
            description: New description (optional, press Enter to keep current)

        Returns:
            Task: Updated task instance

        Raises:
            TaskNotFoundError: If task ID doesn't exist in storage
            InvalidTaskDataError: If both title and description are provided as empty
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        task = self._tasks[task_id]

        if title is not None:
            title = title.strip()
            if not title:
                raise InvalidTaskDataError("Title cannot be empty")
            task.title = title

        if description is not None:
            description = description.strip()
            if not description:
                raise InvalidTaskDataError("Description cannot be empty")
            task.description = description

        return task

    def toggle_status(self, task_id: int) -> Task:
        """
        Toggle a task's completion status.

        Args:
            task_id: ID of task to toggle

        Returns:
            Task: Updated task instance with flipped is_complete status

        Raises:
            TaskNotFoundError: If task ID doesn't exist in storage
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        task = self._tasks[task_id]
        task.is_complete = not task.is_complete
        return task

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task from storage.

        Args:
            task_id: ID of task to delete

        Raises:
            TaskNotFoundError: If task ID doesn't exist in storage
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        del self._tasks[task_id]
