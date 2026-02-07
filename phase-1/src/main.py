"""
Main entry point for the Todo In-Memory Python Console Application.
Initializes components and starts the application loop.
"""

from services import TaskService
from cli import TodoCLI, run_cli


def main():
    """
    Main application entry point.
    Initializes TaskService and starts the CLI interface.
    """
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Application is exiting.")


if __name__ == "__main__":
    main()