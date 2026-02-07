"""
MCP Server for Todo Application
Exposes task operations as tools for AI agents
"""
import asyncio
import sys
import os
# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Optional
from mcp.server import Server
from mcp.types import CallToolResult, TextContent
from pydantic import Field
import json
from datetime import datetime
from sqlmodel import Session, select
from database import get_session
from models.task import Task as TaskModel
from schemas.task import TaskCreate


# Initialize MCP Server
mcp_server = Server("todo-mcp-server")


def get_task_by_id(session: Session, task_id: str, user_id: str):
    """Helper function to get a task by ID for a specific user"""
    task = session.exec(
        select(TaskModel).where(TaskModel.id == int(task_id)).where(TaskModel.user_id == user_id)
    ).first()
    return task


def create_task(session: Session, user_id: str, task_data: TaskCreate):
    """Helper function to create a task"""
    task = TaskModel(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed or False,
        priority=task_data.priority or "medium",
        tags=[],  # Simplified - not using tags for now
        due_date=task_data.due_date
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_tasks(session: Session, user_id: str, completed: Optional[bool] = None):
    """Helper function to get tasks for a user with optional filter"""
    query = select(TaskModel).where(TaskModel.user_id == user_id)

    if completed is not None:
        query = query.where(TaskModel.completed == completed)

    tasks = session.exec(query).all()
    return tasks


def update_task(session: Session, task_id: str, user_id: str, task_data: TaskCreate):
    """Helper function to update a task"""
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    # Update the task with the provided data
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed or task.completed
    task.priority = task_data.priority or task.priority
    task.due_date = task_data.due_date

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, task_id: str, user_id: str):
    """Helper function to delete a task"""
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: str, user_id: str):
    """Helper function to toggle task completion status"""
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    # Toggle the completion status
    task.completed = not task.completed

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@mcp_server.tools.register(
    name="add_task",
    description="Add a new task for a user",
)
async def add_task_handler(
    user_id: str = Field(..., description="The user's ID"),
    title: str = Field(..., description="The task title"),
    description: Optional[str] = Field(None, description="The task description"),
    priority: str = Field("medium", description="Priority level (low, medium, high)"),
    due_date: Optional[str] = Field(None, description="Due date in YYYY-MM-DD format")
) -> CallToolResult:
    """Add a new task using helper functions"""

    with next(get_session()) as session:
        try:
            # Create task data using the schema expected by the service
            task_create_data = TaskCreate(
                title=title,
                description=description,
                priority=priority,
                due_date=datetime.fromisoformat(due_date) if due_date else None,
                completed=False  # Default to not completed
            )

            task = create_task(session, user_id, task_create_data)

            result = {
                "success": True,
                "task_id": str(task.id),
                "message": f"Task '{task.title}' added successfully!"
            }

            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])
        except ValueError as e:
            # Handle datetime parsing errors
            result = {
                "success": False,
                "error": str(e),
                "message": f"Invalid date format: {str(e)}"
            }
            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "message": f"Failed to add task: {str(e)}"
            }
            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])


@mcp_server.tools.register(
    name="list_tasks",
    description="List tasks for a user with optional status filter",
)
async def list_tasks_handler(
    user_id: str = Field(..., description="The user's ID"),
    completed: Optional[bool] = Field(None, description="Filter by completion status")
) -> CallToolResult:
    """List tasks using helper functions"""

    with next(get_session()) as session:
        try:
            # Get tasks using helper function
            tasks = get_tasks(session, user_id, completed)

            tasks_list = []
            for task in tasks:
                tasks_list.append({
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "tags": task.tags,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })

            result = {
                "success": True,
                "tasks": tasks_list,
                "count": len(tasks_list),
                "message": f"Found {len(tasks_list)} tasks"
            }

            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "message": f"Failed to list tasks: {str(e)}"
            }
            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])


@mcp_server.tools.register(
    name="complete_task",
    description="Mark a task as completed",
)
async def complete_task_handler(
    user_id: str = Field(..., description="The user's ID"),
    task_id: str = Field(..., description="The task ID to complete")
) -> CallToolResult:
    """Complete a task using helper functions"""

    with next(get_session()) as session:
        try:
            # Toggle task completion using helper function
            task = toggle_task_completion(session, task_id, user_id)
            if not task:
                result = {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or you don't have permission to modify it"
                }
                return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])

            result = {
                "success": True,
                "task_id": str(task.id),
                "completed": task.completed,
                "message": f"Task '{task.title}' marked as {'completed' if task.completed else 'incomplete'}!"
            }

            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "message": f"Failed to update task completion: {str(e)}"
            }
            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])


@mcp_server.tools.register(
    name="delete_task",
    description="Delete a task",
)
async def delete_task_handler(
    user_id: str = Field(..., description="The user's ID"),
    task_id: str = Field(..., description="The task ID to delete")
) -> CallToolResult:
    """Delete a task using helper functions"""

    with next(get_session()) as session:
        try:
            # Delete task using helper function
            success = delete_task(session, task_id, user_id)

            if not success:
                result = {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or you don't have permission to delete it"
                }
                return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])

            result = {
                "success": True,
                "task_id": str(task_id),
                "message": f"Task deleted successfully!"
            }

            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "message": f"Failed to delete task: {str(e)}"
            }
            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])


@mcp_server.tools.register(
    name="update_task",
    description="Update a task's properties",
)
async def update_task_handler(
    user_id: str = Field(..., description="The user's ID"),
    task_id: str = Field(..., description="The task ID to update"),
    title: Optional[str] = Field(None, description="New title"),
    description: Optional[str] = Field(None, description="New description"),
    priority: Optional[str] = Field(None, description="New priority level"),
    due_date: Optional[str] = Field(None, description="New due date in YYYY-MM-DD format"),
    completed: Optional[bool] = Field(None, description="New completion status")
) -> CallToolResult:
    """Update a task using helper functions"""

    with next(get_session()) as session:
        try:
            # First, get the existing task to preserve unchanged values
            existing_task = get_task_by_id(session, task_id, user_id)
            if not existing_task:
                result = {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or you don't have permission to modify it"
                }
                return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])

            # Create update data using the existing values as defaults
            task_update_data = TaskCreate(
                title=title if title is not None else existing_task.title,
                description=description if description is not None else existing_task.description,
                priority=priority if priority is not None else existing_task.priority,
                due_date=datetime.fromisoformat(due_date) if due_date else existing_task.due_date,
                completed=completed if completed is not None else existing_task.completed
            )

            # Update task using helper function
            task = update_task(session, task_id, user_id, task_update_data)
            if not task:
                result = {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or you don't have permission to modify it"
                }
                return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])

            result = {
                "success": True,
                "task_id": str(task.id),
                "message": f"Task '{task.title}' updated successfully!"
            }

            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])
        except ValueError as e:
            # Handle datetime parsing errors
            result = {
                "success": False,
                "error": str(e),
                "message": f"Invalid date format: {str(e)}"
            }
            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "message": f"Failed to update task: {str(e)}"
            }
            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])


# Health check endpoint
@mcp_server.list_prompts()
async def list_prompts():
    """Return a simple health check"""
    return []


if __name__ == "__main__":
    import uvicorn

    # Run the MCP server
    uvicorn.run(mcp_server.app, host="0.0.0.0", port=8001)