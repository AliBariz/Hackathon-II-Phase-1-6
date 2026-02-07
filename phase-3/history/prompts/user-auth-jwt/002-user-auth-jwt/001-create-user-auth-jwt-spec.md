---
id: 3
title: "Create User Authentication with JWT Spec"
stage: spec
created: 2026-01-07
updated: 2026-01-07
---

# Create User Authentication with JWT Spec

## PROMPT_TEXT

```
- Backend verifies:
  - Token signature
  - Token expiry
  - User identity

---

### 4.3 Authorization Rules

- All API routes require authentication
- Users may only:
  - Read their own tasks
  - Modify their own tasks
  - Delete their own tasks
- User ID in the URL must match the JWT user ID
- Violations return `403 Forbidden`

---

## 5. API Specification

### 5.1 Base Rules

- All routes are prefixed with `/api`
- All responses are JSON
- Requests without JWT return `401 Unauthorized`

---

### 5.2 Endpoints

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/{user_id}/tasks` | List all user tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{id}` | Retrieve task |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

---

### 5.3 Query Parameters (GET /tasks)

- `search`: keyword
- `status`: `pending` | `completed`
- `priority`: `high` | `medium` | `low`
- `tag`: string
- `sort`: `title` | `priority` | `date`

---

## 6. Data Model

### 6.1 User

- Managed by Better Auth
- Identified by unique string ID

### 6.2 Task

Each task must include:

- `id` (integer, primary key)
- `user_id` (string, foreign key)
- `title` (string, required)
- `description` (text, optional)
- `priority` (enum)
- `tags` (array of strings)
- `completed` (boolean)
- `created_at` (timestamp)
- `updated_at` (timestamp)

---

## 7. Frontend Requirements

- Built using **Next.js 16+ App Router**
- Fully responsive layout
- Authentication handled via Better Auth
- All API calls:
  - Use a centralized API client
  - Attach JWT token automatically
- UI must support:
  - Task CRUD
  - Search, filter, and sort
  - Visual status indicators

---

## 8. Backend Requirements

- Built with **FastAPI**
- Uses **SQLModel** for ORM
- Connects to **Neon PostgreSQL**
- JWT verification middleware is mandatory
- All database queries must be user-scoped

---

## 9. Repository & Structure

- Monorepo layout is mandatory
- Specs live under `/specs`
- Claude Code instructions are defined in:
  - Root `CLAUDE.md`
  - `frontend/CLAUDE.md`
  - `backend/CLAUDE.md`

---

## 10. Development Workflow

1. Write or update spec in `/specs`
2. Reference spec using `@specs/...`
3. Ask Claude Code to implement
4. Claude Code reads:
   - Specs
   - Constitution
   - Relevant CLAUDE.md files
5. Claude implements frontend and backend
6. Changes require spec updates first

---

## 11. Acceptance Criteria

Phase II is considered complete when:

- All features are implemented via specs
- Authentication is enforced everywhere
- Users cannot access others' data
- API matches the defined contract
- Frontend and backend are fully integrated
- No manual code was written

---

## 12. Non-Negotiable Rule

> **The specification is the source of truth.
> Any behavior not described here is out of scope.**
```

## RESPONSE_TEXT

Created a comprehensive specification for the user authentication with JWT feature based on the provided requirements. The specification includes:

- Three prioritized user stories covering registration/login (P1), secure task management (P1), and advanced filtering (P2)
- Functional requirements (FR-001 to FR-014) covering authentication, authorization, task CRUD operations, and data isolation
- Key entities (User and Task) with their attributes and relationships
- Success criteria (SC-001 to SC-006) with measurable outcomes for authentication success rates, data isolation, response times, and error handling
- Edge cases for token expiration, invalid tokens, and concurrent access
- A quality checklist verifying the specification meets all requirements

The specification is technology-agnostic in its success criteria while maintaining specific functional requirements for the authentication and task management system. It properly enforces user isolation and security requirements as specified in the input.