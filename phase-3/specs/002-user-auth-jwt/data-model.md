# Data Model: User Authentication with JWT

## Entities

### Task
**Description**: Represents a user's task with all required attributes

**Fields**:
- `id` (integer, primary key, auto-increment)
- `user_id` (string, foreign key, required) - Links to Better Auth user ID
- `title` (string, required) - Task title
- `description` (text, optional) - Task description
- `completed` (boolean, required, default: false) - Completion status
- `priority` (enum: low/medium/high, required, default: medium) - Task priority
- `tags` (array of strings, optional) - Task tags/categories
- `due_date` (date, optional) - Task due date
- `created_at` (timestamp, required) - Creation timestamp
- `updated_at` (timestamp, required) - Last update timestamp

**Validation Rules**:
- Title must be 1-255 characters
- Priority must be one of: low, medium, high
- User_id must match authenticated user's ID
- Due date must be in the future (if provided)

**Relationships**:
- One User to Many Tasks (via user_id foreign key)

### User (Managed by Better Auth)
**Description**: Represents an authenticated user, managed by Better Auth

**Fields**:
- `id` (string, primary key) - Better Auth user ID
- `email` (string) - User's email
- `created_at` (timestamp) - Account creation time

**Relationships**:
- One User to Many Tasks (via user_id in Task entity)

## State Transitions

### Task State Transitions
- **Creation**: New task with `completed = false`
- **Completion**: Task status changes from `completed = false` to `completed = true`
- **Reversion**: Task status changes from `completed = true` to `completed = false`
- **Update**: Any field except `id` and `user_id` can be modified
- **Deletion**: Task is removed from database

## Database Schema

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    tags TEXT[],
    due_date DATE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

### Constraints
- All tasks must have a valid user_id
- User_id cannot be modified after creation
- Title cannot be empty
- Only authenticated users can create/read/update/delete tasks
- Users can only access tasks with matching user_id