import jwt
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlmodel import Session
from database import get_session
from models.task import Task, TaskStatus, TaskPriority, TaskTag
from services.task_service import TaskService
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

@router.get("/{user_id}/search/", response_model=List[Task])
def search_tasks(
    user_id: int,
    q: str = Query(..., min_length=1, max_length=100, description="Search query for title or description"),
    status: TaskStatus = Query(None, description="Filter by status"),
    priority: TaskPriority = Query(None, description="Filter by priority"),
    tag: TaskTag = Query(None, description="Filter by tag"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Search tasks by keyword with query parameter handling for a specific user
    Matches against both title and description in a case-insensitive manner
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to search tasks for this user")

    try:
        # Validate search query
        if len(q) > 100:
            raise HTTPException(status_code=422, detail="Search query must be 100 characters or less")

        # Search tasks using the service method which handles case-insensitive matching
        tasks = TaskService.get_tasks(
            session=session,
            user_id=user_id,
            status=status,
            priority=priority,
            tag=tag,
            search_term=q,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return tasks
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching tasks: {str(e)}")