from typing import List, Optional
from sqlmodel import Session, select
from models.task import Task, TaskStatus, TaskPriority, TaskTag
from datetime import datetime

class TaskService:
    @staticmethod
    def create_task(session: Session, task_data: dict) -> Task:
        """
        Create a new task with the provided data
        """
        task = Task(
            title=task_data.get('title'),
            description=task_data.get('description'),
            status=task_data.get('status', TaskStatus.pending),
            priority=task_data.get('priority', TaskPriority.medium),
            tag=task_data.get('tag', TaskTag.work),
            due_date=task_data.get('due_date'),
            user_id=task_data.get('user_id')  # Add user_id to the task
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID
        """
        return session.get(Task, task_id)

    @staticmethod
    def get_tasks(
        session: Session,
        user_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        tag: Optional[TaskTag] = None,
        search_term: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> List[Task]:
        """
        Retrieve tasks with optional filters
        """
        statement = select(Task).where(Task.user_id == user_id)  # Only get tasks for the specified user

        # Apply filters if provided
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if tag:
            statement = statement.where(Task.tag == tag)

        # Apply search if provided (case-insensitive search)
        if search_term:
            search_pattern = f"%{search_term}%"
            statement = statement.where(
                Task.title.ilike(search_pattern) |
                Task.description.ilike(search_pattern)
            )

        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "desc":
                statement = statement.order_by(Task.due_date.desc())
            else:
                statement = statement.order_by(Task.due_date.asc())
        elif sort_by == "priority":
            if sort_order == "desc":
                statement = statement.order_by(Task.priority.desc())
            else:
                statement = statement.order_by(Task.priority.asc())
        elif sort_by == "title":
            if sort_order == "desc":
                statement = statement.order_by(Task.title.desc())
            else:
                statement = statement.order_by(Task.title.asc())
        else:  # default to created_at
            if sort_order == "desc":
                statement = statement.order_by(Task.created_at.desc())
            else:
                statement = statement.order_by(Task.created_at.asc())

        return session.exec(statement).all()

    @staticmethod
    def update_task(session: Session, task_id: int, task_data: dict) -> Optional[Task]:
        """
        Update a task with the provided data
        """
        task = session.get(Task, task_id)
        if not task:
            return None

        # Update fields if provided
        for field, value in task_data.items():
            if hasattr(task, field) and value is not None:
                setattr(task, field, value)

        # Update the timestamp
        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int) -> bool:
        """
        Delete a task by its ID
        """
        task = session.get(Task, task_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_status(session: Session, task_id: int) -> Optional[Task]:
        """
        Toggle the status of a task between pending and completed
        """
        task = session.get(Task, task_id)
        if not task:
            return None

        # Toggle status
        if task.status == TaskStatus.pending:
            task.status = TaskStatus.completed
        else:
            task.status = TaskStatus.pending

        task.updated_at = datetime.now()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task