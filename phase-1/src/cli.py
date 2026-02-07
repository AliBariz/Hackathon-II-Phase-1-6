"""
Command-line interface for the Todo In-Memory Python Console Application.
Handles user input and output for all task operations.
"""

from services import TaskService


class TodoCLI:
    """
    Command-line interface for the todo application.
    Manages user interaction and input validation.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the CLI with a task service.

        Args:
            task_service (TaskService): The service to handle task operations
        """
        self.task_service = task_service

    def display_menu(self):
        """Display the main menu with all available options."""
        print("\nTodo Application Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print()

    def get_user_choice(self) -> int:
        """
        Get and validate user menu choice.

        Returns:
            int: The user's menu choice (1-7)
        """
        while True:
            try:
                choice = int(input("Enter your choice (1-7): "))
                if 1 <= choice <= 7:
                    return choice
                else:
                    print("Please enter a number between 1 and 7.")
            except ValueError:
                print("Please enter a valid number.")

    def get_task_id(self) -> int:
        """
        Get and validate a task ID from user input.

        Returns:
            int: The validated task ID
        """
        while True:
            try:
                task_id = int(input("Enter task ID: "))
                if task_id > 0:
                    return task_id
                else:
                    print("Task ID must be a positive integer.")
            except ValueError:
                print("Please enter a valid integer for task ID.")

    def get_task_input(self) -> tuple:
        """
        Get title and description input from user with validation.

        Returns:
            tuple: (title: str, description: str or None)
        """
        while True:
            title = input("Enter task title: ").strip()
            if not title:
                print("Title cannot be empty. Please enter a title.")
                continue
            if len(title) > 100:
                print(f"Title exceeds maximum length of 100 characters. Please enter a shorter title.")
                continue
            break

        description_input = input("Enter task description (optional, press Enter to skip): ").strip()
        description = description_input if description_input else None

        if description and len(description) > 500:
            print(f"Description exceeds maximum length of 500 characters. Please enter a shorter description.")
            return self.get_task_input()  # Recursively get input again

        return title, description

    def add_task_flow(self):
        """Execute the Add Task flow with input validation."""
        print("\n--- Add New Task ---")
        try:
            title, description = self.get_task_input()
            task = self.task_service.add_task(title, description)
            print(f"Task added successfully with ID: {task.id}")
        except ValueError as e:
            print(f"Error adding task: {e}")

    def view_tasks_flow(self):
        """Execute the View Tasks flow."""
        print("\n--- All Tasks ---")
        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            description = task.description if task.description else "No description"
            print(f"ID: {task.id} | {status} | {task.title} | {description}")

    def update_task_flow(self):
        """Execute the Update Task flow with task ID validation."""
        print("\n--- Update Task ---")
        task_id = self.get_task_id()

        try:
            # Get the current task to show existing values
            current_task = self.task_service.get_task(task_id)
            print(f"Current task: {current_task.title}")

            # Get new input from user
            title_input = input(f"Enter new title (current: '{current_task.title}', press Enter to keep current): ").strip()
            description_input = input(f"Enter new description (current: '{current_task.description or 'No description'}', press Enter to keep current): ").strip()

            # Prepare update parameters - only update if user provided new value
            new_title = title_input if title_input else None
            new_description = description_input if description_input else None

            # If user entered an empty string for description, that means they want to clear it
            if description_input == "":
                new_description = ""

            task = self.task_service.update_task(task_id, new_title, new_description)
            print(f"Task updated successfully.")
        except ValueError as e:
            print(f"Error updating task: {e}")

    def delete_task_flow(self):
        """Execute the Delete Task flow with task ID validation."""
        print("\n--- Delete Task ---")
        task_id = self.get_task_id()

        try:
            success = self.task_service.delete_task(task_id)
            if success:
                print(f"Task with ID {task_id} deleted successfully.")
            else:
                print(f"Task with ID {task_id} does not exist.")
        except Exception as e:
            print(f"Error deleting task: {e}")

    def mark_complete_flow(self):
        """Execute the Mark Complete flow with task ID validation."""
        print("\n--- Mark Task Complete ---")
        task_id = self.get_task_id()

        try:
            current_task = self.task_service.get_task(task_id)
            if not current_task.completed:
                # Only toggle if it's currently incomplete
                task = self.task_service.toggle_task_completion(task_id)
                print(f"Task with ID {task_id} marked as complete.")
            else:
                print(f"Task with ID {task_id} is already complete.")
        except ValueError as e:
            print(f"Error marking task complete: {e}")

    def mark_incomplete_flow(self):
        """Execute the Mark Incomplete flow with task ID validation."""
        print("\n--- Mark Task Incomplete ---")
        task_id = self.get_task_id()

        try:
            current_task = self.task_service.get_task(task_id)
            if current_task.completed:
                # Only toggle if it's currently complete
                task = self.task_service.toggle_task_completion(task_id)
                print(f"Task with ID {task_id} marked as incomplete.")
            else:
                print(f"Task with ID {task_id} is already incomplete.")
        except ValueError as e:
            print(f"Error marking task incomplete: {e}")

    def run(self):
        """Main application loop for the CLI interface."""
        print("Welcome to the Todo Application!")

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == 1:
                self.add_task_flow()
            elif choice == 2:
                self.view_tasks_flow()
            elif choice == 3:
                self.update_task_flow()
            elif choice == 4:
                self.delete_task_flow()
            elif choice == 5:
                self.mark_complete_flow()
            elif choice == 6:
                self.mark_incomplete_flow()
            elif choice == 7:
                print("Thank you for using the Todo Application. Goodbye!")
                break


def run_cli():
    """Convenience function to run the CLI with a fresh task service."""
    task_service = TaskService()
    cli = TodoCLI(task_service)
    cli.run()