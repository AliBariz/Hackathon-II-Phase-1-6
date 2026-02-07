from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, min_length=1, max_length=50)
    email: str = Field(unique=True, min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=255)  # Hashed password
    created_at: datetime = Field(default_factory=datetime.now)