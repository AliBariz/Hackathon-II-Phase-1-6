"""
Simple Chat API endpoint for AI agent integration
Handles conversation persistence and task operations without complex imports
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
from models.task import Task as TaskModel  # Direct import from models

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


def create_task_direct(session: Session, user_id: str, title: str, description: str = None, priority: str = "medium"):
    """Direct function to create a task without using TaskService"""
    from schemas.task import TaskCreate
    task_data = TaskCreate(
        title=title,
        description=description or "Added via AI assistant",
        priority=priority,
        completed=False
    )

    new_task = TaskModel(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed or False,
        priority=task_data.priority or "medium",
        tags=[],  # Simplified - not using tags for now
        due_date=task_data.due_date
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


def get_tasks_direct(session: Session, user_id: str):
    """Direct function to get tasks without using TaskService"""
    query = select(TaskModel).where(TaskModel.user_id == user_id)
    tasks = session.exec(query).all()
    return tasks


def get_task_direct(session: Session, task_id: str, user_id: str):
    """Direct function to get a task without using TaskService"""
    task = session.exec(
        select(TaskModel).where(TaskModel.id == int(task_id)).where(TaskModel.user_id == user_id)
    ).first()
    return task


def update_task_direct(session: Session, task_id: str, user_id: str, title: str = None, description: str = None, priority: str = None, completed: bool = None):
    """Direct function to update a task without using TaskService"""
    task = get_task_direct(session, task_id, user_id)

    if not task:
        return None

    # Update the task with provided data
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if priority is not None:
        task.priority = priority
    if completed is not None:
        task.completed = completed

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task_direct(session: Session, task_id: str, user_id: str):
    """Direct function to delete a task without using TaskService"""
    task = get_task_direct(session, task_id, user_id)

    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def toggle_task_completion_direct(session: Session, task_id: str, user_id: str):
    """Direct function to toggle task completion without using TaskService"""
    task = get_task_direct(session, task_id, user_id)

    if not task:
        return None

    # Toggle the completion status
    task.completed = not task.completed

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint that:
    1. Processes user message
    2. Executes task operations based on message content
    3. Returns appropriate response
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

                # Create a new task using direct function
                new_task = create_task_direct(session, user_id, task_title)

                final_response = f"I've added the task '{new_task.title}' to your list (Task ID: {new_task.id})."
            else:
                final_response = "I can help you add a task. Please say something like 'Add a task to buy groceries' or 'Create a task called finish report'."

        elif any(word in user_message for word in ["list", "show", "view", "my", "tasks"]):
            # List all tasks for the user using direct function
            tasks = get_tasks_direct(session, user_id)

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

                # Toggle task completion using direct function
                task = toggle_task_completion_direct(session, task_id, user_id)

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

                # Delete the task using direct function
                success = delete_task_direct(session, task_id, user_id)

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

                # Update the task using direct function
                updated_task = update_task_direct(session, task_id, user_id, title=new_title)

                if updated_task:
                    final_response = f"I've updated the task with ID {task_id} to '{updated_task.title}'."
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