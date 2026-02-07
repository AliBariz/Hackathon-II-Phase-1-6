from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import enum

class TaskStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"

class TaskPriority(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TaskTag(str, enum.Enum):
    work = "work"
    home = "home"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=100, min_length=1)
    description: Optional[str] = Field(default=None, max_length=100)
    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    tag: TaskTag = Field(default=TaskTag.work)
    due_date: Optional[datetime] = Field(default=None)
    user_id: int = Field(index=True)  # Foreign key reference to User
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __init__(self, **kwargs):
        # Perform validation during initialization
        title = kwargs.get('title')
        if title and len(title) > 100:
            raise ValueError("Title must be 100 characters or less")

        description = kwargs.get('description')
        if description and len(description) > 100:
            raise ValueError("Description must be 100 characters or less")

        super().__init__(**kwargs)