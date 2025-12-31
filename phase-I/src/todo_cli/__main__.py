"""
Main entry point for todo CLI application.

This module initializes the CLI interface and starts
the main application loop.
"""

from todo_cli.cli.interface import TaskCLI


def main() -> None:
    """Main entry point - starts the CLI application."""
    cli = TaskCLI()
    cli.run()


if __name__ == "__main__":
    main()
