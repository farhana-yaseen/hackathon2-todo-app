"""
CLI interface for todo application.

This module provides the menu-driven user interface that
handles user interaction, input parsing, and coordinates with TaskManager.
"""


from todo_cli.cli.formatter import TaskFormatter
from todo_cli.core.exceptions import InvalidTaskDataError, TaskNotFoundError
from todo_cli.core.task_manager import TaskManager


class TaskCLI:
    """
    Menu-driven CLI interface for todo application.

    Handles all user interaction, menu display, input parsing,
    and delegates to TaskManager for business logic.
    """

    def __init__(self) -> None:
        """Initialize CLI with TaskManager instance."""
        self.manager = TaskManager()

    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n--- TODO APPLICATION ---")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Complete")
        print("6. Exit")
        print("")

    def get_menu_choice(self) -> int:
        """
        Get and validate menu choice from user.

        Returns:
            int: Validated menu choice (1-6)
        """
        while True:
            choice = input("Selection: ").strip()

            if not choice:
                continue

            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= 6:
                    return choice_num

            print(f"Invalid choice: {choice}. Please enter a number between 1 and 6.")

    def get_task_id(self, prompt: str) -> int:
        """
        Get and validate task ID from user input.

        Args:
            prompt: Message to display before asking for ID

        Returns:
            int: Validated task ID
        """
        while True:
            user_input = input(prompt).strip()

            if not user_input:
                continue

            if user_input.isdigit():
                return int(user_input)

            print("Invalid input. Please enter a numeric task ID.")

    def view_tasks(self) -> None:
        """Display all tasks using TaskManager and TaskFormatter."""
        tasks = self.manager.view_tasks()
        print(TaskFormatter.format_task_list(tasks))

    def add_task(self) -> None:
        """Handle Add Task operation."""
        print("\n--- Add Task ---")

        title = input("Title: ").strip()
        if not title:
            print(TaskFormatter.format_error("Title cannot be empty"))
            return

        description = input("Description: ").strip()
        if not description:
            print(TaskFormatter.format_error("Description cannot be empty"))
            return

        try:
            task = self.manager.add_task(title, description)
            print(TaskFormatter.format_confirmation(f"Task added: [{task.id}] {task.title}"))
        except InvalidTaskDataError as e:
            print(TaskFormatter.format_error(str(e)))

    def update_task(self) -> None:
        """Handle Update Task operation."""
        print("\n--- Update Task ---")

        task_id = self.get_task_id("Enter task ID to update: ")

        new_title = input("New title (press Enter to keep current): ").strip()
        new_description = input("New description (press Enter to keep current): ").strip()

        if not new_title and not new_description:
            print(TaskFormatter.format_error("At least title or description must be provided"))
            return

        try:
            updated_task = self.manager.update_task(
                task_id, new_title, new_description
            )
            msg = f"Task updated: [{updated_task.id}] {updated_task.title}"
            print(TaskFormatter.format_confirmation(msg))
        except (TaskNotFoundError, InvalidTaskDataError) as e:
            print(TaskFormatter.format_error(str(e)))

    def toggle_complete(self) -> None:
        """Handle Toggle Complete operation."""
        print("\n--- Toggle Complete ---")

        task_id = self.get_task_id("Enter task ID to toggle: ")

        try:
            updated_task = self.manager.toggle_status(task_id)
            status_text = "complete" if updated_task.is_complete else "pending"
            msg = f"Task {updated_task.id} marked as {status_text}"
            print(TaskFormatter.format_confirmation(msg))
        except TaskNotFoundError as e:
            print(TaskFormatter.format_error(str(e)))

    def delete_task(self) -> None:
        """Handle Delete Task operation."""
        print("\n--- Delete Task ---")

        task_id = self.get_task_id("Enter task ID to delete: ")

        try:
            self.manager.delete_task(task_id)
            print(TaskFormatter.format_confirmation(f"Task #{task_id} deleted successfully"))
        except TaskNotFoundError as e:
            print(TaskFormatter.format_error(str(e)))

    def run(self) -> None:
        """Main application loop - displays menu and handles user choices."""
        print("NOTE: Tasks are stored in memory only and will be lost when you exit.\n")

        while True:
            self.display_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.view_tasks()
            elif choice == 2:
                self.add_task()
            elif choice == 3:
                self.update_task()
            elif choice == 4:
                self.delete_task()
            elif choice == 5:
                self.toggle_complete()
            elif choice == 6:
                confirm = input("Are you sure you want to exit? (yes/no): ").strip().lower()
                if confirm in ["yes", "y"]:
                    print("Goodbye!")
                    break
                # If not confirmed, loop continues
