# Tasks: User Authentication with JWT

## Feature Overview
**Feature**: User Authentication with JWT for full-stack todo application
**Branch**: 002-user-auth-jwt
**Spec**: [specs/002-user-auth-jwt/spec.md](specs/002-user-auth-jwt/spec.md)
**Plan**: [specs/002-user-auth-jwt/plan.md](specs/002-user-auth-jwt/plan.md)
**Priority Order**: US1 (P1) → US2 (P1) → US3 (P2)

## Phase 1: Setup & Monorepo Foundation
**Goal**: Establish monorepo structure and initial project setup

- [x] T001 Create monorepo structure: frontend/, backend/, specs/
- [x] T002 Create root CLAUDE.md with project overview and workflow
- [x] T003 Create frontend/CLAUDE.md with Next.js patterns and UI rules
- [x] T004 Create backend/CLAUDE.md with FastAPI structure and SQLModel rules
- [x] T005 Initialize README.md with setup instructions and feature explanation
- [x] T006 Create .spec-kit/config.yaml with project configuration
- [x] T007 Set up basic package.json in frontend with Next.js dependencies
- [x] T008 Set up requirements.txt in backend with FastAPI and SQLModel dependencies

## Phase 2: Database Foundation & Authentication Setup
**Goal**: Establish database connection, user management, and authentication foundation

- [x] T009 [P] Configure Neon PostgreSQL connection in backend with DATABASE_URL
- [x] T010 [P] Set up SQLModel ORM configuration in backend/models/__init__.py
- [x] T011 [P] Create Task model in backend/models/task.py with all required fields
- [x] T012 [P] Create Task schema in backend/schemas/task.py for requests/responses
- [x] T013 [P] Configure database tables and indexes per data model specification
- [x] T014 [P] Create Better Auth configuration in frontend for JWT issuance
- [x] T015 [P] Implement JWT middleware in backend for token verification
- [x] T016 [P] Create centralized API client in frontend/lib/api.ts with JWT handling

## Phase 3: User Registration and Login (US1 - P1)
**Goal**: Enable user registration and authentication to access personalized todo system
**Independent Test**: Can register a new user account and log in successfully, delivering the core value of personalized task management

- [x] T017 [US1] Create login page component in frontend/pages/login.tsx
- [x] T018 [US1] Create registration page component in frontend/pages/register.tsx
- [x] T019 [US1] Implement JWT token storage and retrieval in frontend
- [x] T020 [US1] Create authentication service in backend/services/auth.py
- [x] T021 [US1] Test user registration flow with email and password validation
- [ ] T022 [US1] Test user login flow with JWT token issuance
- [ ] T023 [US1] Test session persistence across page refreshes

## Phase 4: Secure Task Management (US2 - P1)
**Goal**: Enable authenticated users to perform CRUD operations on their own tasks with proper user isolation
**Independent Test**: A logged-in user can create tasks, view them, update them, and delete them, ensuring data isolation from other users

- [ ] T024 [US2] Create GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py
- [ ] T025 [US2] Create POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py
- [ ] T026 [US2] Create GET /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py
- [ ] T027 [US2] Create PUT /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py
- [ ] T028 [US2] Create DELETE /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py
- [ ] T029 [US2] Create PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/routes/tasks.py
- [ ] T030 [US2] Implement user ownership validation in all task endpoints
- [ ] T031 [US2] Create Task service in backend/services/task_service.py with CRUD operations
- [ ] T032 [US2] Create TaskList component in frontend/components/TaskList.tsx
- [ ] T033 [US2] Create TaskForm component in frontend/components/TaskForm.tsx
- [ ] T034 [US2] Create dashboard page in frontend/pages/dashboard.tsx to display tasks
- [ ] T035 [US2] Implement task creation API call in frontend with JWT authentication
- [ ] T036 [US2] Implement task listing API call in frontend with JWT authentication
- [ ] T037 [US2] Implement task update API call in frontend with JWT authentication
- [ ] T038 [US2] Implement task deletion API call in frontend with JWT authentication
- [ ] T039 [US2] Implement task completion toggle in frontend with JWT authentication
- [ ] T040 [US2] Test that users can only access their own tasks (user isolation)
- [ ] T041 [US2] Test CRUD operations work correctly for authenticated users
- [ ] T042 [US2] Test proper 403 Forbidden responses when accessing other users' tasks

## Phase 5: Advanced Task Features with Filtering (US3 - P2)
**Goal**: Enable authenticated users to search, filter, and sort their tasks by various criteria
**Independent Test**: A user with multiple tasks can apply various filters and sorting options, seeing only their own filtered results

- [ ] T043 [US3] Enhance GET /api/{user_id}/tasks endpoint with search functionality
- [ ] T044 [US3] Enhance GET /api/{user_id}/tasks endpoint with filtering by status
- [ ] T045 [US3] Enhance GET /api/{user_id}/tasks endpoint with filtering by priority
- [ ] T046 [US3] Enhance GET /api/{user_id}/tasks endpoint with filtering by tag
- [ ] T047 [US3] Enhance GET /api/{user_id}/tasks endpoint with sorting options
- [ ] T048 [US3] Update Task service with search, filter, and sort methods
- [ ] T049 [US3] Create search and filter UI in frontend/components/TaskList.tsx
- [ ] T050 [US3] Implement search API call in frontend with query parameters
- [ ] T051 [US3] Implement filtering UI controls in frontend
- [ ] T052 [US3] Implement sorting UI controls in frontend
- [ ] T053 [US3] Test search functionality returns only user's matching tasks
- [ ] T054 [US3] Test filtering functionality returns only user's filtered tasks
- [ ] T055 [US3] Test sorting functionality correctly orders user's tasks

## Phase 6: Quality Validation & Testing
**Goal**: Validate all functionality meets requirements and quality standards

- [ ] T056 Validate authentication: users cannot access other users' tasks
- [ ] T057 Validate JWT required for all endpoints (401 responses)
- [ ] T058 Test complete CRUD workflow: create → view → update → delete → complete
- [ ] T059 Validate filtering, sorting, search match query parameters exactly
- [ ] T060 Validate data persistence across page reloads and backend restarts
- [ ] T061 Test frontend responsiveness across different device sizes
- [ ] T062 Validate structured logging implementation (FR-015)
- [ ] T063 Validate basic metrics tracking (FR-016)
- [ ] T064 Validate error tracking implementation (FR-017)
- [ ] T065 Test JWT token expiration handling
- [ ] T066 Test malformed JWT token handling
- [ ] T067 Test access to non-existent task IDs
- [ ] T068 Verify no import/export functionality is implemented (FR-018)
- [ ] T069 Test concurrent requests with same token

## Phase 7: Polish & Cross-Cutting Concerns
**Goal**: Final integration, documentation, and preparation for submission

- [ ] T070 Implement logout functionality in frontend with JWT cleanup
- [ ] T071 Handle JWT expiry by redirecting to login in frontend
- [ ] T072 Add secure password hashing and storage implementation (FR-019)
- [ ] T073 Implement secure session management (FR-020)
- [ ] T074 Add audit logging for sensitive operations (FR-021)
- [ ] T075 Update README.md with complete setup and usage instructions
- [ ] T076 Create quickstart guide with environment setup instructions
- [ ] T077 Test complete end-to-end workflow: Login → create task → filter/sort → update → complete → delete
- [ ] T078 Verify frontend-backend consistency and integration
- [ ] T079 Prepare repository for submission with all required components

## Dependencies
**User Story Order**: US1 → US2 → US3 (US2 and US3 depend on US1 for authentication foundation)

## Parallel Execution Examples
- **US1 Tasks**: T017-T023 can be developed in parallel with backend auth service (T020) and frontend components (T017-T019)
- **US2 Tasks**: Backend API endpoints (T024-T029) can be developed in parallel with frontend components (T032-T038)
- **US3 Tasks**: Backend enhancements (T043-T047) can be developed in parallel with frontend UI updates (T049-T052)

## Implementation Strategy
- **MVP Scope**: Complete US1 (authentication) + US2 (basic task CRUD) for minimal viable product
- **Incremental Delivery**: Each user story provides independent value and can be tested separately
- **Quality Focus**: Each phase includes validation tasks to ensure requirements are met