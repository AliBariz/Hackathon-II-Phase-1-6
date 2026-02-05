# Data Model: Todo In-Memory Python Console Application

**Feature**: Todo In-Memory Python Console Application
**Date**: 2025-12-31
**Modeler**: Claude Code

## Entity Definitions

### Task Entity

**Description**: Core entity representing a single to-do item in the application

**Attributes**:
- `id`: Integer (required, unique, positive)
  - Sequential identifier starting from 1
  - Primary key for the task
  - Used for all operations (update, delete, mark complete)
- `title`: String (required, max 100 characters)
  - Short description of the task
  - Cannot be empty
  - Must be validated for length
- `description`: String (optional, max 500 characters)
  - Detailed information about the task
  - Can be empty/None
  - Must be validated for length if provided
- `completed`: Boolean (required, default: False)
  - Tracks completion status
  - False = incomplete, True = complete
  - Toggled via mark complete/incomplete operations

**Validation Rules**:
- ID must be a positive integer
- Title must be 1-100 characters (non-empty)
- Description, if provided, must be ≤ 500 characters
- Completed must be a boolean value

**State Transitions**:
- `incomplete` → `complete` (via mark complete operation)
- `complete` → `incomplete` (via mark incomplete operation)

### TaskList Collection

**Description**: In-memory collection managing all tasks

**Attributes**:
- `tasks`: Dictionary mapping ID to Task objects
  - Key: Integer ID
  - Value: Task object
  - Provides O(1) lookup performance
- `next_id`: Integer (auto-incrementing)
  - Tracks the next available ID
  - Starts at 1, increments with each new task

**Operations**:
- `add_task(title, description)`: Creates and adds a new task
- `get_task(task_id)`: Retrieves a task by ID
- `update_task(task_id, title, description)`: Updates task fields
- `delete_task(task_id)`: Removes a task
- `mark_complete(task_id)`: Sets completed status to True
- `mark_incomplete(task_id)`: Sets completed status to False
- `get_all_tasks()`: Returns all tasks

**Constraints**:
- All IDs must be unique within the collection
- Task count limited by available memory
- No persistence outside of application runtime

## Relationships

### Task to TaskList
- One-to-many relationship
- Each Task belongs to exactly one TaskList
- TaskList contains multiple Tasks
- TaskList manages Task lifecycle

## Data Flow

### Creation Flow
1. User provides title (and optional description)
2. System validates input length and content
3. System assigns next available ID
4. Task object is created with completed=False
5. Task is added to TaskList collection

### Retrieval Flow
1. User provides task ID
2. System validates ID format and existence
3. Task is retrieved from collection
4. Task data is presented to user

### Update Flow
1. User provides task ID and new field values
2. System validates ID and new values
3. Task fields are updated in collection
4. Success is confirmed to user

### Deletion Flow
1. User provides task ID
2. System validates ID and confirms existence
3. Task is removed from collection
4. Success is confirmed to user

## Error Conditions

### Validation Errors
- Invalid input length (title > 100 chars, description > 500 chars)
- Missing required fields (title)
- Invalid ID format (non-numeric)
- Non-existent task ID

### State Errors
- Attempting operations on deleted tasks
- Duplicate ID assignment (should not occur with proper ID management)