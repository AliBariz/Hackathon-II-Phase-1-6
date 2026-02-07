from fastapi import APIRouter
from api.endpoints import tasks, search, auth

# Create the main API router
api_router = APIRouter()

# Include the auth-related routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Include the task-related routes (these now have user_id in the path)
api_router.include_router(tasks.router, prefix="", tags=["tasks"])  # No prefix since paths include user_id
api_router.include_router(search.router, prefix="", tags=["search"])  # No prefix since paths include user_id