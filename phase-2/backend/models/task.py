from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")
    tags: Optional[str] = Field(default=None)  # Store as JSON string for simplicity
    due_date: Optional[datetime] = Field(default=None)
    user_id: str = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    """
    Task model representing a user's task with all required attributes
    """
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship: One User to Many Tasks (via user_id foreign key)