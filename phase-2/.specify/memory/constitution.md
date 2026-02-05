<!--
Sync Impact Report:
- Version change: 2.0.0 → 3.0.0 (major update - adding multi-user authentication and authorization)
- Modified principles: Updated to include multi-user support and authentication requirements
- Added sections: Authentication & Security Model, REST API Contract with JWT, User Isolation
- Removed sections: Previous restrictions on authentication and user accounts
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
  - README.md ⚠ pending
- Follow-up TODOs: None
-->

# Phase II – Multi-User Todo Web Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All code must originate from a specification file; No manual coding is allowed; Every feature must be traceable back to a documented specification; The workflow follows: Write Specification → Generate Plan → Break Plan into Tasks → Implement via Claude Code → Iterate only through spec updates.

### II. Full-Stack Architecture with Authentication
The project must follow a clean separation between frontend and backend: Next.js for frontend with Better Auth, FastAPI for backend, SQLModel for ORM, and Neon PostgreSQL for database; No mixing of technology stacks; Strict separation of concerns between UI, business logic, and data layers; Authentication must be handled via JWT tokens between frontend and backend.

### III. Mandatory Technology Stack with Authentication
The application must use the specified technology stack exclusively: Next.js 16+ (App Router) (frontend), Python FastAPI (backend), SQLModel (ORM), Neon Serverless PostgreSQL (database), Better Auth (authentication), REST (communication); No alternative frameworks or additional stacks are allowed; All components must integrate properly with the mandated stack.

### IV. Multi-User Feature Completeness
The application must implement all Phase II features completely for multiple authenticated users: task creation, listing, updating, deletion, completion toggling, priorities (low/medium/high), tags/categories, search, filter, sorting, persistent database storage, and responsive web-based UI; Each feature must work correctly without errors; User isolation must be enforced.

### V. Data Persistence with User Isolation
All tasks must be stored persistently in Neon PostgreSQL database with user_id association; No in-memory storage allowed; No file-based persistence allowed; Data must survive application restarts and be accessible across sessions; Users must only access their own data.

### VI. Clean Code and Architecture Standards
All generated code must follow framework best practices for Next.js, FastAPI, SQLModel, and Better Auth; Use clear, descriptive names; Follow proper separation of concerns between models, schemas, routes, services; Be maintainable and extensible without technical debt; Authentication and authorization must be implemented correctly.

## Technical Constraints

### Project Scope
- Multi-user Todo web application with authenticated access only
- Neon Serverless PostgreSQL database storage only (no in-memory, no file storage)
- Next.js 16+ (App Router) frontend with FastAPI backend
- Authentication via Better Auth with JWT tokens
- Forbidden: real-time features, mobile apps (except web-based)

### Required Technology Stack
- Next.js 16+ (App Router) for frontend
- Python FastAPI for backend API
- SQLModel for ORM/models
- Neon Serverless PostgreSQL for database
- Better Auth for authentication
- REST (JSON) for communication
- No additional tooling without explicit spec approval

### Authentication & Security Model
- Authentication is handled by Better Auth on the Next.js frontend
- Better Auth must be configured to issue JWT tokens
- Both frontend and backend must share the same JWT secret (BETTER_AUTH_SECRET)
- FastAPI backend must verify JWT signature and decode user identity
- User isolation must be enforced through task ownership

### Functional Requirements
Each task must contain: id (integer), title (string), description (string), completed (boolean), priority (enum: low/medium/high), category/tag (string), due_date (date), created_at (timestamp), user_id (integer)
- Priorities must be stored, editable, and usable for filtering/sorting (default: medium)
- Categories must be stored persistently, editable, and filterable
- Search must work on title and description (case-insensitive, partial-match)
- Filters must work by completion status, priority, category, due date (combinable)
- Sorting must work by due date, priority, alphabetical (deterministic, after filters)
- All operations must enforce user ownership of tasks

## Development Workflow

### Project Structure Requirements
The repository must follow this exact structure:
```
/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── CLAUDE.md
├── frontend/
│   ├── CLAUDE.md
│   └── (Next.js app)
├── backend/
│   ├── CLAUDE.md
│   └── (FastAPI app)
├── docker-compose.yml
└── README.md
```

Each file must have single responsibility; Circular dependencies are forbidden; No application logic outside of designated layers.

### REST API Contract
All endpoints require a valid JWT and return JSON:
- GET `/api/{user_id}/tasks` - List all tasks for user
- POST `/api/{user_id}/tasks` - Create new task for user
- GET `/api/{user_id}/tasks/{id}` - Get task details for user
- PUT `/api/{user_id}/tasks/{id}` - Update task for user
- DELETE `/api/{user_id}/tasks/{id}` - Delete task for user
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle completion for user
- All endpoints enforce that `{user_id}` matches JWT user ID (mismatch → 403 Forbidden)
- Requests without token return 401 Unauthorized

### Error Handling Standards
- Invalid input must never crash the app
- Backend must never expose stack traces to frontend
- Frontend must handle API failures gracefully
- Empty states must be clearly communicated to the user
- Proper HTTP status codes must be returned for all API endpoints
- Authentication failures must be handled appropriately

## Governance

This constitution is the highest authority in the repository; If any file, plan, or instruction conflicts with this constitution, this constitution takes precedence. All code must be generated by Claude Code, traceable back to a specification file, and justifiable via a documented plan. The project is complete only when all Phase II features work correctly (multi-user, priorities, tags, search, filter, sort), data persists in Neon DB with proper user isolation, frontend and backend are cleanly separated with secure authentication, no forbidden features exist, app is stable and usable, and repository contains all required deliverables.

**Version**: 3.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2026-01-07