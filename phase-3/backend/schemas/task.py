from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Base schema for task
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # Enum: low, medium, high
    tags: Optional[List[str]] = None  # Store as array of strings
    due_date: Optional[datetime] = None

# Schema for creating a task
class TaskCreate(TaskBase):
    title: str  # Required field for creation

# Schema for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None  # Enum: low, medium, high
    tags: Optional[List[str]] = None  # Store as array of strings
    due_date: Optional[datetime] = None

# Schema for completing a task
class TaskComplete(BaseModel):
    completed: bool

from pydantic import BaseModel, field_validator

# Schema for the response (includes computed fields)
class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    tags: Optional[List[str]] = None  # Convert from DB string to list
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator('tags', mode='before')
    @classmethod
    def validate_tags(cls, v):
        if isinstance(v, str) and v.startswith('{') and v.endswith('}'):
            # Handle PostgreSQL array format: {tag1,tag2,tag3}
            if v == '{}':
                return []
            else:
                # Remove curly braces and split
                content = v[1:-1]  # Remove first { and last }
                return [tag.strip('"\'') for tag in content.split(',') if tag.strip()]
        elif isinstance(v, list):
            # Already a list
            return v
        elif v is None:
            return []
        else:
            return v