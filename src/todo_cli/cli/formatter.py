"""
CLI output formatter for task display.

This module handles formatting of task lists, status indicators,
and user-facing messages.
"""


from todo_cli.models.task import Task


class TaskFormatter:
    """
    Formats tasks for CLI display with status indicators and text wrapping.
    """

    @staticmethod
    def format_status(is_complete: bool) -> str:
        """
        Format status indicator based on completion status.

        Args:
            is_complete: Task completion status

        Returns:
            str: Status indicator (`[x]` for complete, `[ ]` for pending)
        """
        return "[x]" if is_complete else "[ ]"

    @staticmethod
    def format_task(task: Task) -> str:
        """
        Format a single task for display.

        Args:
            task: Task instance to format

        Returns:
            str: Formatted task string with ID, status, title, and description
        """
        status = TaskFormatter.format_status(task.is_complete)
        title = TaskFormatter._truncate_text(task.title, max_length=30)
        description = task.description

        return f"[{task.id:3d}] {status} {title}: {description}"

    @staticmethod
    def _truncate_text(text: str, max_length: int) -> str:
        """
        Truncate text to specified length with ellipsis if needed.

        Args:
            text: Text to truncate
            max_length: Maximum allowed length

        Returns:
            str: Truncated text with ellipsis if shortened
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."

    @staticmethod
    def format_task_list(tasks: list[Task]) -> str:
        """
        Format all tasks for display.

        Args:
            tasks: List of tasks to format

        Returns:
            str: Formatted task list, one task per line
        """
        if not tasks:
            return "No tasks yet. Add your first task!"

        formatted_tasks = [TaskFormatter.format_task(task) for task in tasks]
        return "\n".join(formatted_tasks)

    @staticmethod
    def format_confirmation(message: str) -> str:
        """
        Format a success/confirmation message.

        Args:
            message: Message to format

        Returns:
            str: Formatted message with checkmark
        """
        return f"✓ {message}"

    @staticmethod
    def format_error(message: str) -> str:
        """
        Format an error message.

        Args:
            message: Error message to format

        Returns:
            str: Formatted error message with cross mark
        """
        return f"✗ {message}"
