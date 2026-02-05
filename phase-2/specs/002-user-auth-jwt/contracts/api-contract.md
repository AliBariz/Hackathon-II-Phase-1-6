# API Contract: User Authentication with JWT Todo API

## Base URL
`/api/{user_id}`

## Authentication
All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

## Common Response Format
All responses return JSON with the following structure:
```json
{
  "success": true,
  "data": { ... },
  "message": "optional message"
}
```

For errors:
```json
{
  "success": false,
  "error": "error message",
  "code": "error code"
}
```

## Endpoints

### GET /api/{user_id}/tasks
**Description**: List all tasks for a user

**Path Parameters**:
- `user_id` (string, required): User ID to retrieve tasks for

**Query Parameters**:
- `search` (string, optional): Keyword to search in title/description
- `status` (string, optional): Filter by completion status (pending/completed)
- `priority` (string, optional): Filter by priority (high/medium/low)
- `tag` (string, optional): Filter by tag
- `sort` (string, optional): Sort by (title/priority/date)

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user_id": "user123",
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "priority": "high",
      "tags": ["work", "important"],
      "due_date": "2023-12-31",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id doesn't match JWT user ID)
- 404: User not found

### POST /api/{user_id}/tasks
**Description**: Create a new task for a user

**Path Parameters**:
- `user_id` (string, required): User ID to create task for

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Task description",
  "priority": "medium",
  "tags": ["tag1", "tag2"],
  "due_date": "2023-12-31",
  "completed": false
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "priority": "medium",
    "tags": ["tag1", "tag2"],
    "due_date": "2023-12-31",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

**Status Codes**:
- 201: Created
- 400: Bad Request (invalid input)
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id doesn't match JWT user ID)

### GET /api/{user_id}/tasks/{id}
**Description**: Get a specific task for a user

**Path Parameters**:
- `user_id` (string, required): User ID
- `id` (integer, required): Task ID

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "priority": "medium",
    "tags": ["tag1", "tag2"],
    "due_date": "2023-12-31",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id doesn't match JWT user ID)
- 404: Task not found

### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task for a user

**Path Parameters**:
- `user_id` (string, required): User ID
- `id` (integer, required): Task ID

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "priority": "high",
  "tags": ["updated", "tags"],
  "due_date": "2023-12-31",
  "completed": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "priority": "high",
    "tags": ["updated", "tags"],
    "due_date": "2023-12-31",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

**Status Codes**:
- 200: Success
- 400: Bad Request (invalid input)
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id doesn't match JWT user ID)
- 404: Task not found

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task for a user

**Path Parameters**:
- `user_id` (string, required): User ID
- `id` (integer, required): Task ID

**Response**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id doesn't match JWT user ID)
- 404: Task not found

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle completion status of a specific task for a user

**Path Parameters**:
- `user_id` (string, required): User ID
- `id` (integer, required): Task ID

**Request Body**:
```json
{
  "completed": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user123",
    "completed": true
  }
}
```

**Status Codes**:
- 200: Success
- 400: Bad Request (invalid input)
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id doesn't match JWT user ID)
- 404: Task not found