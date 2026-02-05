# Quickstart Guide: Todo In-Memory Python Console Application

**Feature**: Todo In-Memory Python Console Application
**Date**: 2025-12-31
**Version**: 1.0

## Overview

This guide provides instructions for setting up and running the menu-driven console todo application. The application allows users to manage tasks in memory with five core operations: Add, View, Update, Delete, and Mark Complete/Incomplete.

## Prerequisites

- Python 3.13 or higher
- UV package manager (for dependency management)
- Command-line interface access

## Setup Instructions

### 1. Environment Setup

```bash
# Install UV package manager (if not already installed)
pip install uv

# Navigate to project directory
cd /path/to/your/project

# Install dependencies (if any are added later)
uv pip install -r requirements.txt
```

### 2. Project Structure

The application follows this structure:
```
src/
├── __init__.py
├── main.py          # Application entry point
├── models.py        # Task data models
├── services.py      # Business logic
└── cli.py           # Command-line interface
```

### 3. Running the Application

```bash
# Run the application
uv run python src/main.py

# Or directly with Python
python src/main.py
```

## Usage Guide

### Main Menu Options

Once the application starts, you'll see a menu with the following options:

```
Todo Application Menu:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit
```

### Operation Details

#### 1. Add Task
- Prompts for task title (required, max 100 characters)
- Prompts for task description (optional, max 500 characters)
- Automatically assigns a unique ID
- Sets initial status to "Incomplete"

#### 2. View Tasks
- Displays all tasks in the system
- Shows ID, title, description, and completion status
- If no tasks exist, displays appropriate message

#### 3. Update Task
- Prompts for task ID
- Prompts for new title and/or description
- Updates only the fields provided (leaves others unchanged)
- Validates input length before updating

#### 4. Delete Task
- Prompts for task ID
- Confirms deletion before proceeding
- Removes task from the system

#### 5. Mark Task Complete
- Prompts for task ID
- Changes task status to "Complete"
- Validates that task exists before changing status

#### 6. Mark Task Incomplete
- Prompts for task ID
- Changes task status to "Incomplete"
- Validates that task exists before changing status

#### 7. Exit
- Safely exits the application
- All data will be lost (in-memory only)

## Input Validation

### Character Limits
- **Title**: Maximum 100 characters (required)
- **Description**: Maximum 500 characters (optional)

### Error Handling
- Invalid inputs are caught gracefully
- Clear error messages are displayed
- Application does not crash on invalid input
- Users are prompted to re-enter valid input

## Example Workflow

1. Run the application: `python src/main.py`
2. Select "1. Add Task"
3. Enter title: "Buy groceries"
4. Enter description: "Milk, bread, eggs, fruits"
5. Select "2. View Tasks" to see your task
6. Select "5. Mark Task Complete" to update status
7. Continue using other features as needed
8. Select "7. Exit" to close the application

## Troubleshooting

### Common Issues

**Application won't start**
- Verify Python 3.13+ is installed
- Check that all required files exist in src/ directory

**Input validation errors**
- Ensure titles are 1-100 characters
- Ensure descriptions are ≤ 500 characters
- Verify task IDs are numeric and exist

**Menu not responding**
- Check that you're entering valid menu options (1-7)
- Verify numeric input for task IDs

## Development Notes

### Architecture
- **Models**: Handle data structure and validation
- **Services**: Implement business logic
- **CLI**: Manage user interface and input/output
- **Main**: Coordinate application flow

### Error Handling
- All user inputs are validated
- Invalid operations are handled gracefully
- No stack traces shown to users
- Clear error messages provided

### Testing Strategy
- Unit tests for each module
- Integration tests for complete workflows
- Input validation tests
- Error handling verification