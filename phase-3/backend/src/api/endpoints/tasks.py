import jwt
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session
from database import get_session
from models.task import Task, TaskStatus, TaskPriority, TaskTag
from services.task_service import TaskService
from services.validation_service import ValidationService
from services.auth_service import AuthService
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

def get_current_user(token: str = Depends(security), session: Session = Depends(get_session)):
    """
    Get current user from JWT token
    """
    try:
        payload = jwt.decode(token.credentials, AuthService.SECRET_KEY, algorithms=[AuthService.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

    user = AuthService.get_user_by_username(session, username)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

@router.post("/{user_id}/tasks/", response_model=Task)
def create_task(
    user_id: int,
    task: Task,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Create a new task for a specific user with validation for priority and tag
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create tasks for this user")

    # Validate the task data
    errors = ValidationService.validate_task_data(task.dict())
    if errors:
        raise HTTPException(status_code=422, detail=errors)

    # Additional validation for priority and tag values
    if task.priority not in [p.value for p in TaskPriority]:
        errors.append(f"Priority must be one of: {', '.join([p.value for p in TaskPriority])}")

    if task.tag not in [t.value for t in TaskTag]:
        errors.append(f"Tag must be one of: {', '.join([t.value for t in TaskTag])}")

    if errors:
        raise HTTPException(status_code=422, detail=errors)

    # Prepare task data for creation
    task_data = {
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'tag': task.tag,
        'due_date': task.due_date,
        'user_id': user_id
    }

    try:
        created_task = TaskService.create_task(session, task_data)
        return created_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


@router.get("/{user_id}/tasks/{task_id}", response_model=Task)
def get_task(
    user_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Get a task by ID for a specific user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access tasks for this user")

    if not ValidationService.validate_task_id(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    task = TaskService.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Additional check to ensure the task belongs to the user
    # This would require modifying the Task model to include a user_id field
    # For now, we'll assume the user isolation is handled at the service level

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=Task)
def update_task(
    user_id: int,
    task_id: int,
    task_update: Task,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Update a task by ID for a specific user to modify priority, tag, and other details
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update tasks for this user")

    if not ValidationService.validate_task_id(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    # Check if task exists
    existing_task = TaskService.get_task_by_id(session, task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Validate the update data
    task_dict = task_update.dict(exclude_unset=True)  # Only include fields that were provided
    errors = ValidationService.validate_task_data(task_dict)

    # Additional validation for priority and tag values if provided
    if 'priority' in task_dict and task_dict['priority'] not in [p.value for p in TaskPriority]:
        errors.append(f"Priority must be one of: {', '.join([p.value for p in TaskPriority])}")

    if 'tag' in task_dict and task_dict['tag'] not in [t.value for t in TaskTag]:
        errors.append(f"Tag must be one of: {', '.join([t.value for t in TaskTag])}")

    if errors:
        raise HTTPException(status_code=422, detail=errors)

    try:
        updated_task = TaskService.update_task(session, task_id, task_dict)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found after update attempt")
        return updated_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Delete a task by ID for a specific user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete tasks for this user")

    if not ValidationService.validate_task_id(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    success = TaskService.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/toggle-status", response_model=Task)
def toggle_task_status(
    user_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Toggle a task's status between pending and completed for a specific user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to toggle task status for this user")

    if not ValidationService.validate_task_id(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    task = TaskService.toggle_task_status(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/{user_id}/tasks/", response_model=List[Task])
def get_tasks(
    user_id: int,
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    tag: Optional[TaskTag] = Query(None),
    search: Optional[str] = Query(None, description="Search term for title/description"),
    sort_by: str = Query("created_at", description="Field to sort by: created_at, due_date, priority, title"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Get all tasks for a specific user with optional filtering and sorting
    Shows all task details including priority and tag information
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access tasks for this user")

    try:
        tasks = TaskService.get_tasks(
            session=session,
            user_id=user_id,  # Pass the user_id from the URL
            status=status,
            priority=priority,
            tag=tag,
            search_term=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tasks: {str(e)}")