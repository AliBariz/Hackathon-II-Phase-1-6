from typing import Dict, Any, List
from models.task import TaskStatus, TaskPriority, TaskTag
from datetime import datetime

class ValidationService:
    @staticmethod
    def validate_task_data(task_data: Dict[str, Any]) -> List[str]:
        """
        Validates task data and returns a list of validation errors.
        Returns empty list if validation passes.
        """
        errors = []

        # Validate title
        title = task_data.get('title')
        if not title:
            errors.append("Title is required")
        elif len(title) > 100:
            errors.append("Title must be 100 characters or less")

        # Validate description
        description = task_data.get('description')
        if description and len(description) > 100:
            errors.append("Description must be 100 characters or less")

        # Validate status
        status = task_data.get('status')
        if status and status not in [s.value for s in TaskStatus]:
            errors.append(f"Status must be one of: {', '.join([s.value for s in TaskStatus])}")

        # Validate priority
        priority = task_data.get('priority')
        if priority and priority not in [p.value for p in TaskPriority]:
            errors.append(f"Priority must be one of: {', '.join([p.value for p in TaskPriority])}")

        # Validate tag
        tag = task_data.get('tag')
        if tag and tag not in [t.value for t in TaskTag]:
            errors.append(f"Tag must be one of: {', '.join([t.value for t in TaskTag])}")

        # Validate due date
        due_date = task_data.get('due_date')
        if due_date:
            try:
                # Try to parse the date if it's a string
                if isinstance(due_date, str):
                    datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                elif not isinstance(due_date, datetime):
                    errors.append("Due date must be a valid datetime")
            except ValueError:
                errors.append("Due date must be a valid datetime")

        return errors

    @staticmethod
    def validate_user_id(user_id: Any) -> bool:
        """
        Validates that the user_id is a positive integer.
        """
        try:
            user_id_int = int(user_id)
            return user_id_int > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_task_id(task_id: Any) -> bool:
        """
        Validates that the task_id is a positive integer.
        """
        try:
            task_id_int = int(task_id)
            return task_id_int > 0
        except (ValueError, TypeError):
            return False