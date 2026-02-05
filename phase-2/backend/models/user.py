from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, sa_column_kwargs={"index": True})
    password_hash: str = Field(nullable=False)  # Store hashed password


class User(UserBase, table=True):
    """
    User model managed by Better Auth
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships can be defined here if needed