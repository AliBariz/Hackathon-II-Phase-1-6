from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """
    Service class for handling task-related business logic and database operations.
    """

    @staticmethod
    def get_tasks(
        session: Session,
        user_id: str,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        sort: str = "created_at",
        order: str = "desc"
    ) -> List[Task]:
        """
        Get all tasks for a specific user with optional filtering, searching, and sorting.
        """
        query = select(Task).where(Task.user_id == user_id)

        # Apply filters based on query parameters
        if completed is not None:
            query = query.where(Task.completed == completed)

        if priority is not None:
            query = query.where(Task.priority == priority)

        if tag is not None:
            query = query.where(Task.tags.contains(tag))

        if search is not None:
            query = query.where(
                (Task.title.contains(search)) |
                (Task.description.contains(search))
            )

        # Apply sorting
        if sort == "created_at":
            if order == "asc":
                query = query.order_by(Task.created_at)
            else:
                query = query.order_by(Task.created_at.desc())
        elif sort == "updated_at":
            if order == "asc":
                query = query.order_by(Task.updated_at)
            else:
                query = query.order_by(Task.updated_at.desc())
        elif sort == "priority":
            if order == "asc":
                query = query.order_by(Task.priority)
            else:
                query = query.order_by(Task.priority.desc())
        elif sort == "title":
            if order == "asc":
                query = query.order_by(Task.title)
            else:
                query = query.order_by(Task.title.desc())
        else:
            # Default sorting by created_at descending
            query = query.order_by(Task.created_at.desc())

        # Execute the query
        tasks = session.exec(query).all()
        return tasks

    @staticmethod
    def get_task(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a specific user.
        """
        task = session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()
        return task

    @staticmethod
    def create_task(session: Session, user_id: str, task_data: TaskCreate) -> Task:
        """
        Create a new task for a specific user.
        """
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed or False,
            priority=task_data.priority or "medium",
            tags=task_data.tags or [],
            due_date=task_data.due_date
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def update_task(session: Session, task_id: str, user_id: str, task_data: TaskCreate) -> Optional[Task]:
        """
        Update a specific task by ID for a specific user.
        """
        task = session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()

        if not task:
            return None

        # Update the task with the provided data
        task.title = task_data.title
        task.description = task_data.description
        task.completed = task_data.completed or task.completed
        task.priority = task_data.priority or task.priority
        task.tags = task_data.tags or task.tags
        task.due_date = task_data.due_date

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a specific task by ID for a specific user.
        """
        task = session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()

        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Toggle the completion status of a specific task by ID for a specific user.
        """
        task = session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()

        if not task:
            return None

        # Toggle the completion status
        task.completed = not task.completed

        session.add(task)
        session.commit()
        session.refresh(task)

        return task