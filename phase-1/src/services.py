"""
Task service for the Todo In-Memory Python Console Application.
Implements business logic for task operations using the Task model.
"""

from models import Task, TaskList


class TaskService:
    """
    Service responsible for managing tasks in memory.

    Responsibilities:
    - Maintain an in-memory list of tasks
    - Generate sequential unique IDs per runtime
    - Enforce existence checks
    """

    def __init__(self):
        """Initialize the TaskService with an empty TaskList."""
        self.task_list = TaskList()

    def add_task(self, title: str, description: str = None) -> Task:
        """
        Creates and adds a new task to the collection.

        Args:
            title (str): Required title (max 100 characters)
            description (str, optional): Optional description (max 500 characters)

        Returns:
            Task: The newly created Task object
        """
        return self.task_list.add_task(title, description)

    def get_all_tasks(self) -> list:
        """
        Returns all tasks in the collection.

        Returns:
            list: List of all Task objects
        """
        return self.task_list.get_all_tasks()

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Task:
        """
        Updates task fields.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title if provided
            description (str, optional): New description if provided

        Returns:
            Task: The updated Task object

        Raises:
            ValueError: If task ID doesn't exist
        """
        return self.task_list.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Removes a task from the collection.

        Args:
            task_id (int): The ID of the task to remove

        Returns:
            bool: True if task was successfully deleted, False if task didn't exist
        """
        return self.task_list.delete_task(task_id)

    def toggle_task_completion(self, task_id: int) -> Task:
        """
        Toggles the completion status of a task.

        Args:
            task_id (int): The ID of the task to toggle

        Returns:
            Task: The updated Task object

        Raises:
            ValueError: If task ID doesn't exist
        """
        if task_id not in self.task_list.tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task = self.task_list.tasks[task_id]
        if task.completed:
            return self.task_list.mark_incomplete(task_id)
        else:
            return self.task_list.mark_complete(task_id)

    def get_task(self, task_id: int) -> Task:
        """
        Retrieves a task by ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task: The requested Task object

        Raises:
            ValueError: If task ID doesn't exist
        """
        return self.task_list.get_task(task_id)

    def mark_complete(self, task_id: int) -> Task:
        """
        Sets completed status to True.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            Task: The updated Task object

        Raises:
            ValueError: If task ID doesn't exist
        """
        return self.task_list.mark_complete(task_id)

    def mark_incomplete(self, task_id: int) -> Task:
        """
        Sets completed status to False.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            Task: The updated Task object

        Raises:
            ValueError: If task ID doesn't exist
        """
        return self.task_list.mark_incomplete(task_id)