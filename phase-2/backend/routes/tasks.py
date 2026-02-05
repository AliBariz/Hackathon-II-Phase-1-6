from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from models.task import Task
from schemas.task import TaskResponse, TaskCreate
from database import get_session
from services.auth import AuthService

router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: str,
    current_user: dict = Depends(AuthService.get_current_user),
    session: Session = Depends(get_session),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high)"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    search: Optional[str] = Query(None, description="Search in title or description"),
    sort: Optional[str] = Query("created_at", description="Sort by field (created_at, updated_at, priority, title)"),
    order: Optional[str] = Query("desc", description="Sort order (asc, desc)")
):
    """
    Get all tasks for the specified user with optional filtering, searching, and sorting.
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    token_user_id = current_user.get("sub")
    if user_id != token_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: Cannot access another user's tasks"
        )

    # Build the query with user_id filter
    query = select(Task).where(Task.user_id == user_id)

    # Apply filters based on query parameters
    if completed is not None:
        query = query.where(Task.completed == completed)

    if priority is not None:
        query = query.where(Task.priority == priority)

    if tag is not None:
        query = query.where(Task.tags.like(f'%{tag}%'))

    if search is not None:
        query = query.where(
            (Task.title.contains(search)) |
            (Task.description.contains(search))
        )

    # Apply sorting
    if sort == "created_at":
        if order == "asc":
            query = query.order_by(Task.created_at)
        else:
            query = query.order_by(Task.created_at.desc())
    elif sort == "updated_at":
        if order == "asc":
            query = query.order_by(Task.updated_at)
        else:
            query = query.order_by(Task.updated_at.desc())
    elif sort == "priority":
        if order == "asc":
            query = query.order_by(Task.priority)
        else:
            query = query.order_by(Task.priority.desc())
    elif sort == "title":
        if order == "asc":
            query = query.order_by(Task.title)
        else:
            query = query.order_by(Task.title.desc())
    else:
        # Default sorting by created_at descending
        query = query.order_by(Task.created_at.desc())

    # Execute the query
    tasks = session.exec(query).all()

    return tasks


@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: dict = Depends(AuthService.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user.
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    token_user_id = current_user.get("sub")
    if user_id != token_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: Cannot create tasks for another user"
        )

    # Create the task with the user_id from the URL
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed or False,
        priority=task_data.priority or "medium",
        tags=task_data.tags or [],
        due_date=task_data.due_date
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: str,
    current_user: dict = Depends(AuthService.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the specified user.
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    token_user_id = current_user.get("sub")
    if user_id != token_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: Cannot access another user's tasks"
        )

    # Find the task by ID and user_id
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: str,
    task_data: TaskCreate,
    current_user: dict = Depends(AuthService.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the specified user.
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    token_user_id = current_user.get("sub")
    if user_id != token_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: Cannot update another user's tasks"
        )

    # Find the task by ID and user_id
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Update the task with the provided data
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed or task.completed
    task.priority = task_data.priority or task.priority
    task.tags = task_data.tags or task.tags
    task.due_date = task_data.due_date

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(
    user_id: str,
    task_id: str,
    current_user: dict = Depends(AuthService.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the specified user.
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    token_user_id = current_user.get("sub")
    if user_id != token_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: Cannot delete another user's tasks"
        )

    # Find the task by ID and user_id
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Delete the task
    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: str,
    task_id: str,
    current_user: dict = Depends(AuthService.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task by ID for the specified user.
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    token_user_id = current_user.get("sub")
    if user_id != token_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: Cannot update another user's tasks"
        )

    # Find the task by ID and user_id
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Toggle the completion status
    task.completed = not task.completed

    session.add(task)
    session.commit()
    session.refresh(task)

    return task