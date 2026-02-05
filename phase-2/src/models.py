"""
Task model for the Todo In-Memory Python Console Application.
Defines the Task data structure with validation rules.
"""

class Task:
    """
    Core entity representing a single to-do item in the application.

    Attributes:
        id (int): Unique positive integer identifier
        title (str): Required string (max 100 characters)
        description (str): Optional string (max 100 characters)
        completed (bool): Boolean indicating completion status (default: False)
    """

    def __init__(self, task_id: int, title: str, description: str = None):
        """
        Initialize a Task instance with validation.

        Args:
            task_id (int): Unique positive integer identifier
            title (str): Required title (max 100 characters)
            description (str, optional): Optional description (max 100 characters)

        Raises:
            ValueError: If validation rules are violated
        """
        # Validate ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError(f"Task ID must be a positive integer, got {task_id}")

        # Validate title
        if not isinstance(title, str):
            raise ValueError(f"Title must be a string, got {type(title)}")
        if len(title) < 1:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError(f"Title exceeds maximum length of 100 characters: {len(title)}")

        # Validate description if provided
        if description is not None:
            if not isinstance(description, str):
                raise ValueError(f"Description must be a string, got {type(description)}")
            if len(description) > 500:
                raise ValueError(f"Description exceeds maximum length of 500 characters: {len(description)}")

        self.id = task_id
        self.title = title
        self.description = description
        self.completed = False  # Default to False as per specification


class TaskList:
    """
    In-memory collection managing all tasks.

    Attributes:
        tasks (dict): Dictionary mapping ID to Task objects
        next_id (int): Auto-incrementing ID tracker
    """

    def __init__(self):
        """Initialize an empty TaskList with ID counter starting at 1."""
        self.tasks = {}
        self.next_id = 1

    def add_task(self, title: str, description: str = None) -> Task:
        """
        Creates and adds a new task to the collection.

        Args:
            title (str): Required title (max 100 characters)
            description (str, optional): Optional description (max 100 characters)

        Returns:
            Task: The newly created Task object
        """
        task = Task(self.next_id, title, description)
        self.tasks[task.id] = task
        self.next_id += 1
        return task

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
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")
        return self.tasks[task_id]

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
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task = self.tasks[task_id]

        # Update title if provided and valid
        if title is not None:
            if not isinstance(title, str):
                raise ValueError(f"Title must be a string, got {type(title)}")
            if len(title) < 1:
                raise ValueError("Title cannot be empty")
            if len(title) > 100:
                raise ValueError(f"Title exceeds maximum length of 100 characters: {len(title)}")
            task.title = title

        # Update description if provided and valid
        if description is not None:
            if not isinstance(description, str):
                raise ValueError(f"Description must be a string, got {type(description)}")
            if len(description) > 500:
                raise ValueError(f"Description exceeds maximum length of 500 characters: {len(description)}")
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Removes a task from the collection.

        Args:
            task_id (int): The ID of the task to remove

        Returns:
            bool: True if task was successfully deleted, False if task didn't exist
        """
        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        return True

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
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task = self.tasks[task_id]
        task.completed = True
        return task

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
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task = self.tasks[task_id]
        task.completed = False
        return task

    def get_all_tasks(self) -> list:
        """
        Returns all tasks in the collection.

        Returns:
            list: List of all Task objects
        """
        return list(self.tasks.values())