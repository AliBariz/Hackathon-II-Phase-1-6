# Data Model: Enhanced Task Management

## Entities

### Task
Represents a to-do item with extended metadata for improved organization.

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `title`: String (Required, Max 100 characters)
- `description`: String (Optional, Max 100 characters)
- `status`: Enum (Required, Values: "pending", "completed")
- `priority`: Enum (Required, Values: "high", "medium", "low")
- `tag`: Enum (Required, Values: "work", "home")
- `due_date`: DateTime (Optional)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, Updates on modification)

**Validation Rules**:
- Title must be non-empty and <= 100 characters
- Description <= 100 characters if provided
- Status must be one of the allowed values
- Priority must be one of the allowed values
- Tag must be one of the allowed values
- Due date must be a valid date if provided

**State Transitions**:
- Creation: status = "pending" by default
- Update: status can transition from "pending" to "completed" and vice versa

### User
Represents the person managing tasks (for future authentication implementation).

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `username`: String (Unique)
- `email`: String (Unique, Valid email format)
- `created_at`: DateTime (Auto-generated)

## Relationships
- One User to Many Tasks (User owns multiple tasks)

## Indexes
- Index on `status` field for efficient filtering
- Index on `priority` field for efficient sorting
- Index on `due_date` field for efficient date-based queries
- Composite index on `(status, priority)` for combined filtering