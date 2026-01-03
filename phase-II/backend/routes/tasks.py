"""Task API routes for Phase II Full-Stack Todo Application.

This module implements RESTful endpoints for Task CRUD operations.
All endpoints require JWT authentication and enforce user data isolation.
"""
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select, and_, func

from models import Task
from db import (
    AuthenticatedUser,
    require_auth,
    get_session,
)


# ========== Pydantic Models ==========

class TaskCreate(BaseModel):
    """Request model for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    reminder_enabled: bool = False
    category: Optional[str] = Field(None, max_length=50)


class TaskUpdate(BaseModel):
    """Request model for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    reminder_enabled: Optional[bool] = None
    category: Optional[str] = Field(None, max_length=50)


class TaskResponse(BaseModel):
    """Response model for a single task."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[datetime]
    reminder_enabled: bool
    category: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Response model for listing tasks."""
    tasks: List[TaskResponse]
    total: int


class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool
    message: str


class CategoryStat(BaseModel):
    """Stat for a single category."""
    category: str
    count: int


class StatsResponse(BaseModel):
    """Response model for task statistics."""
    total_tasks: int
    completed_tasks: int
    active_tasks: int
    overdue_tasks: int
    category_stats: List[CategoryStat]


# ========== Router ==========

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


# ========== Endpoints ==========

@router.get("/stats", response_model=StatsResponse)
async def get_task_stats(
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session),
) -> StatsResponse:
    """Get statistics for the authenticated user's tasks."""
    now = datetime.utcnow()

    # Total tasks
    total_query = select(func.count(Task.id)).where(Task.user_id == user.user_id)
    total_tasks = session.exec(total_query).one()

    # Completed tasks
    completed_query = select(func.count(Task.id)).where(
        and_(Task.user_id == user.user_id, Task.completed == True)
    )
    completed_tasks = session.exec(completed_query).one()

    # Active tasks
    active_tasks = total_tasks - completed_tasks

    # Overdue tasks
    overdue_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == user.user_id,
            Task.completed == False,
            Task.due_date < now
        )
    )
    overdue_tasks = session.exec(overdue_query).one()

    # Category stats
    category_query = (
        select(Task.category, func.count(Task.id))
        .where(Task.user_id == user.user_id)
        .group_by(Task.category)
    )
    category_results = session.exec(category_query).all()

    category_stats = [
        CategoryStat(category=cat if cat else "No Category", count=count)
        for cat, count in category_results
    ]

    return StatsResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        active_tasks=active_tasks,
        overdue_tasks=overdue_tasks,
        category_stats=category_stats,
    )


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session),
) -> TaskListResponse:
    """List all tasks for the authenticated user.

    Returns tasks sorted by creation date (newest first).
    """
    query = (
        select(Task)
        .where(Task.user_id == user.user_id)
        .order_by(Task.created_at.desc())
    )
    tasks = session.exec(query).all()

    return TaskListResponse(
        tasks=[TaskResponse.model_validate(task) for task in tasks],
        total=len(tasks),
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Create a new task for the authenticated user.

    The user_id is automatically set from the JWT token.
    """
    task = Task(
        user_id=user.user_id,
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        reminder_enabled=task_data.reminder_enabled,
        category=task_data.category,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Get a specific task by ID.

    Returns 404 if task not found.
    Returns 403 if task belongs to another user.
    """
    query = select(Task).where(
        and_(
            Task.id == task_id,
            Task.user_id == user.user_id,
        )
    )
    task = session.exec(query).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Update a task's title and/or description.

    Returns 404 if task not found.
    Returns 403 if task belongs to another user.
    """
    query = select(Task).where(
        and_(
            Task.id == task_id,
            Task.user_id == user.user_id,
        )
    )
    task = session.exec(query).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.reminder_enabled is not None:
        task.reminder_enabled = task_data.reminder_enabled
    if task_data.category is not None:
        task.category = task_data.category

    task.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    task_id: int,
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Toggle task completion status.

    Returns 404 if task not found.
    Returns 403 if task belongs to another user.
    """
    query = select(Task).where(
        and_(
            Task.id == task_id,
            Task.user_id == user.user_id,
        )
    )
    task = session.exec(query).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", response_model=SuccessResponse)
async def delete_task(
    task_id: int,
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session),
) -> SuccessResponse:
    """Delete a task.

    Returns 404 if task not found.
    Returns 403 if task belongs to another user.
    """
    query = select(Task).where(
        and_(
            Task.id == task_id,
            Task.user_id == user.user_id,
        )
    )
    task = session.exec(query).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    session.delete(task)
    session.commit()

    return SuccessResponse(
        success=True,
        message=f"Task {task_id} deleted successfully",
    )
