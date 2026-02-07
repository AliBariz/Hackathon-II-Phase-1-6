from sqlmodel import SQLModel

# Import all models to make them available
from .task import Task
from .user import User

# This makes all models available when importing from models
__all__ = ["Task", "User", "SQLModel"]