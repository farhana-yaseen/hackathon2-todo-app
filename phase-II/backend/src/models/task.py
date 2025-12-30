"""Task model for Phase II Full-Stack Todo Application.

This module defines the Task SQLModel entity for Neon PostgreSQL database.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Index


class Task(SQLModel, table=True):
    """Task entity representing a todo item owned by a specific user.

    Attributes:
        id: Unique auto-incrementing task ID
        user_id: ID of the user who owns this task (from Better Auth)
        title: Task heading (1-200 characters, required)
        description: Task details (optional, max 1000 characters)
        completed: Completion status flag
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated

    Note:
        user_id references Better Auth's user ID (string type).
        No foreign key constraint is enforced at DB level since Better Auth
        manages the users table separately.
    """
    id: Optional[int] = Field(default=None, primary_key=True, ge=1)
    user_id: str = Field(
        nullable=False,
        index=True,
        description="User ID from Better Auth (no FK constraint)"
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False,
        description="Task heading (1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        nullable=True,
        description="Task details (optional, max 1000 characters)"
    )
    completed: bool = Field(default=False, description="Completion status flag")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when task was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when task was last updated"
    )

    # Composite index for efficient queries by user and creation date
    __tablename__ = "tasks"

    class Config:
        """Pydantic model configuration."""
        from_attributes = True


# Define composite index for user_id and created_at for efficient task listing
Index("idx_tasks_user_created", Task.user_id, Task.created_at)
