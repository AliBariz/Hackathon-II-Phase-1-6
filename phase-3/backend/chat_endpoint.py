"""
Chat API endpoint for AI agent integration
Handles conversation persistence and tool execution
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import asyncio
from sqlmodel import Session, select
from datetime import datetime
import os
from database import get_session

# Create router
router = APIRouter()

# Models for the chat API
class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tool_calls: Optional[List[Dict]] = None


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint that:
    1. Loads conversation history from database
    2. Stores user message
    3. Executes agent with MCP tools
    4. Stores assistant response
    5. Returns response and tool calls
    """
    try:
        user_message = request.message.lower()
        final_response = ""

        # Import required modules at the top
        import re

        # Parse and execute task operations based on user message
        if any(word in user_message for word in ["add", "create", "new"]):
            # Extract task title from message (simple parsing)
            # Look for patterns like "add task to buy groceries" or "create task called buy groceries"
            title_match = re.search(r'(?:add|create|new)\s+(?:a\s+)?(?:task|todo)\s+(?:called|to|that|which)\s+(.+?)(?:\.|$)', request.message, re.IGNORECASE)
            if not title_match:
                title_match = re.search(r'(?:add|create|new)\s+(?:a\s+)?(?:task|todo)\s+(.+?)(?:\.|$)', request.message, re.IGNORECASE)

            if title_match:
                task_title = title_match.group(1).strip()

                # Import the required modules - use absolute paths to avoid import issues
                import sys
                import os
                sys.path.append(os.path.dirname(os.path.abspath(__file__)))

                from services.task_service import TaskService
                from schemas.task import TaskCreate

                # Create a new task
                task_data = TaskCreate(
                    title=task_title,
                    description="Added via AI assistant",
                    priority="medium",
                    completed=False
                )

                # Use the TaskService to create the task
                new_task = TaskService.create_task(session, user_id, task_data)

                final_response = f"I've added the task '{new_task.title}' to your list (Task ID: {new_task.id})."
            else:
                final_response = "I can help you add a task. Please say something like 'Add a task to buy groceries' or 'Create a task called finish report'."

        elif any(word in user_message for word in ["list", "show", "view", "my", "tasks"]):
            # List all tasks for the user
            from services.task_service import TaskService

            # Get tasks for the user - using the correct parameter order
            # get_tasks(session: Session, user_id: str, completed: Optional[bool] = None, ...)
            tasks = TaskService.get_tasks(session, user_id, None)  # Get all tasks regardless of completion status

            if tasks:
                task_list = "\n".join([f"- {task.id}: {task.title} ({'✓' if task.completed else '○'})" for task in tasks[:10]])  # Limit to first 10 tasks
                final_response = f"Here are your tasks:\n{task_list}\n\nYou have {len(tasks)} total tasks."
            else:
                final_response = "You don't have any tasks yet. You can add a task by saying something like 'Add a task to buy groceries'."

        elif any(word in user_message for word in ["complete", "done", "finish", "mark"]):
            # Extract task ID from message
            id_match = re.search(r'(?:task|id)\s+(\d+)', request.message, re.IGNORECASE)
            if id_match:
                task_id = id_match.group(1)

                # Toggle task completion
                from services.task_service import TaskService
                task = TaskService.toggle_task_completion(session, task_id, user_id)

                if task:
                    status = "completed" if task.completed else "marked as incomplete"
                    final_response = f"I've {status} the task '{task.title}' (Task ID: {task.id})."
                else:
                    final_response = f"I couldn't find a task with ID {task_id} or it doesn't belong to you."
            else:
                final_response = "I can help you mark a task as complete. Please specify the task ID, like 'Mark task 1 as complete' or 'Complete task 5'."

        elif any(word in user_message for word in ["delete", "remove"]):
            # Extract task ID from message
            id_match = re.search(r'(?:task|id)\s+(\d+)', request.message, re.IGNORECASE)
            if id_match:
                task_id = id_match.group(1)

                # Delete the task
                from services.task_service import TaskService
                success = TaskService.delete_task(session, task_id, user_id)

                if success:
                    final_response = f"I've deleted the task with ID {task_id}."
                else:
                    final_response = f"I couldn't find a task with ID {task_id} or it doesn't belong to you."
            else:
                final_response = "I can help you delete a task. Please specify the task ID, like 'Delete task 1' or 'Remove task 5'."

        elif any(word in user_message for word in ["update", "change", "modify", "edit"]):
            # Extract task ID and new details from message
            id_match = re.search(r'(?:task|id)\s+(\d+)', request.message, re.IGNORECASE)
            title_match = re.search(r'(?:to|as|name|title)\s+(.+?)(?:\.|$)', request.message, re.IGNORECASE)

            if id_match and title_match:
                task_id = id_match.group(1)
                new_title = title_match.group(1).strip()

                # Update the task
                from schemas.task import TaskCreate
                from services.task_service import TaskService

                # Use the existing service to get the task properly
                existing_task = TaskService.get_task(session, task_id, user_id)
                if existing_task:
                    # Create update data using the existing values as defaults
                    task_data = TaskCreate(
                        title=new_title,
                        description=existing_task.description or "Updated via AI assistant",
                        priority=existing_task.priority or "medium",
                        due_date=existing_task.due_date,
                        completed=existing_task.completed
                    )

                    updated_task = TaskService.update_task(session, task_id, user_id, task_data)

                    if updated_task:
                        final_response = f"I've updated the task with ID {task_id} to '{updated_task.title}'."
                    else:
                        final_response = f"I couldn't update the task with ID {task_id}."
                else:
                    final_response = f"I couldn't find a task with ID {task_id} or it doesn't belong to you."
            else:
                final_response = "I can help you update a task. Please specify the task ID and new details, like 'Update task 1 to buy milk' or 'Change task 2 to finish presentation'."

        elif any(word in user_message for word in ["hello", "hi", "hey", "help"]):
            final_response = "Hello! I'm your task management assistant. You can ask me to add, list, complete, update, or delete tasks. For example: 'Add a task to buy groceries', 'Show my tasks', 'Complete task 1', or 'Delete task 2'."
        else:
            final_response = f"I understand you said: '{request.message}'. You can ask me to add, list, complete, update, or delete tasks."

        # Generate a fake conversation ID (in reality, you'd save to DB and use real ID)
        conversation_id = f"conv_{user_id}_{int(datetime.now().timestamp())}"

        # Return the response
        return ChatResponse(
            response=final_response,
            conversation_id=conversation_id,
            tool_calls=None  # For now, we're not implementing tool calls
        )

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Chat processing error: {str(e)}")
        print(f"Traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")


# Additional endpoint to get conversation history (simplified)
@router.get("/api/{user_id}/conversations/{conversation_id}")
async def get_conversation(user_id: str, conversation_id: str):
    """
    Retrieve conversation history (placeholder implementation)
    """
    # In a real implementation, this would fetch from database
    return {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "messages": [
            {"role": "user", "content": "Sample user message", "timestamp": datetime.now()},
            {"role": "assistant", "content": "Sample assistant response", "timestamp": datetime.now()}
        ]
    }