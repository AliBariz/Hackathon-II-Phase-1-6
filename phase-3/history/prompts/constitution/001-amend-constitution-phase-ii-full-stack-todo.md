---
id: 1
title: "Amend Constitution to Phase II Full-Stack Todo Application"
stage: constitution
created: 2026-01-07
updated: 2026-01-07
---

# Amend Constitution to Phase II Full-Stack Todo Application

## PROMPT_TEXT

```
# 📜 constitution.md
## Phase II – Full-Stack Todo Application
**Intermediate Level: Organization & Usability**

---

## 1. Purpose of This Constitution

This constitution defines the **absolute rules, constraints, and quality standards** for **Phase II** of the Todo Application, developed for the hackathon.

Its purpose is to ensure:
- Correct interpretation of Phase II requirements
- Clean transition from Phase I to Phase II
- Zero ambiguity in architecture, features, and responsibilities
- Strict separation of frontend, backend, and data layers
- Professional, production-ready implementation standards

This document is the **highest authority** for Phase II.
If any file, plan, task, or implementation conflicts with this constitution, **this constitution takes precedence**.

---

## 2. Phase II Scope Definition

### 2.1 Phase Objective

Upgrade the Todo application into a **full-stack web application** with improved organization, usability, and real-world features, including:

- Priorities
- Tags/Categories
- Search, filter, and sorting
- Persistent database storage
- Web-based UI

---

## 3. Mandatory Technology Stack (Strict)

The following stack is **mandatory and exclusive** for Phase II:

| Layer | Technology |
|-----|-----------|
| Frontend | Next.js |
| Backend API | FastAPI |
| ORM / Models | SQLModel |
| Database | Neon (PostgreSQL) |
| Communication | REST (JSON) |

❌ No alternative frameworks are allowed
❌ No mixing of extra backend or frontend stacks

---

## 4. Functional Requirements (Mandatory)

All features below **must be implemented completely**.

---

### 4.1 Task Core Fields

Each task **must** contain:

| Field | Type | Required |
|-----|------|----------|
| id | integer | Yes |
| title | string | Yes |
| description | string | No |
| completed | boolean | Yes |
| priority | enum (low, medium, high) | Yes |
| category / tag | string | Yes |
| due_date | date | Optional |
| created_at | timestamp | Yes |

---

### 4.2 Priorities

- Each task must have a priority:
  - `low`
  - `medium`
  - `high`
- Default priority: `medium`
- Priority must be:
  - Stored in the database
  - Editable
  - Usable for filtering and sorting

---

### 4.3 Tags / Categories

- Each task must belong to at least one category (e.g., `work`, `home`)
- Categories are string-based (no separate table required unless specified later)
- Categories must be:
  - Stored persistently
  - Editable
  - Filterable

---

### 4.4 Search

- Users must be able to search tasks by keyword
- Search scope:
  - Title
  - Description
- Search must be:
  - Case-insensitive
  - Partial-match based

---

### 4.5 Filtering

Users must be able to filter tasks by:
- Completion status (complete / incomplete)
- Priority
- Category
- Due date (optional)

Filters must work in combination (e.g., `high priority + incomplete`).

---

### 4.6 Sorting

Users must be able to sort tasks by:
- Due date
- Priority
- Alphabetical order (title)

Sorting must be:
- Deterministic
- Applied after filters
- Clearly reflected in the UI

---

## 5. Backend Rules (FastAPI + SQLModel)

### 5.1 API Design

- RESTful endpoints only
- JSON request/response format
- Clear separation between:
  - Models
  - Schemas
  - Routes
  - Services

### 5.2 Data Persistence

- All tasks must be stored in **Neon PostgreSQL**
- No in-memory storage allowed
- No file-based persistence allowed

### 5.3 Validation

- All input must be validated at API level
- Invalid requests must return:
  - Proper HTTP status codes
  - Clear error messages

---

## 6. Frontend Rules (Next.js)

### 6.1 UI Responsibilities

The frontend must:
- Display tasks clearly with priority and category indicators
- Provide controls for:
  - Creating tasks
  - Updating tasks
  - Deleting tasks
  - Searching
  - Filtering
  - Sorting

### 6.2 UX Rules

- UI must clearly show:
  - Task status
  - Priority level
  - Category
- Sorting and filtering must be user-controllable
- No hidden or implicit behavior

---

## 7. Architecture & Separation of Concerns

Strict separation is required:

- Frontend → UI & user interaction only
- Backend → Business logic & validation
- Database → Persistent storage only

❌ No business logic in frontend
❌ No UI logic in backend

---

## 8. Error Handling & Stability

- Application must not crash on invalid input
- Backend must never expose stack traces
- Frontend must handle API failures gracefully
- Empty states must be clearly communicated to the user

---

## 9. Out-of-Scope (Explicitly Forbidden)

The following are **not allowed** in Phase II:

- Authentication & user accounts
- Role-based access control
- Background jobs or queues
- Realtime features (WebSockets)
- Mobile apps
- External third-party APIs (except Neon)

---

## 10. Code Quality Standards

All code must:
- Be readable and well-structured
- Follow framework best practices
- Avoid unused logic and dead code
- Use meaningful naming
- Be maintainable and extensible

---

## 11. Documentation Requirements

The repository **must include**:
- Updated `README.md` with setup instructions
- Clear explanation of features
- Environment setup for Neon DB
- API endpoint documentation (brief)

---

## 12. Acceptance Criteria (Final Gate)

Phase II is considered **complete** only if:

- ✅ All Phase II features are implemented
- ✅ Tasks support priority and category
- ✅ Search, filter, and sorting work correctly
- ✅ Data persists in Neon DB
- ✅ Frontend and backend are cleanly separated
- ✅ App is stable and usable
- ✅ No forbidden features exist

Failure to meet **any single criterion** invalidates the Phase II submission.

---

## 13. Final Authority Statement

This constitution is **binding and final**.

No shortcuts.
No assumptions.
No undocumented behavior.

**Design first. Data second. UI last.**
```

## RESPONSE_TEXT

Updated the project constitution at `.specify/memory/constitution.md` to reflect the Phase II requirements for a full-stack Todo application. The changes included:

- Major version update from 1.0.0 to 2.0.0 due to complete technology stack change
- Replaced Phase I console app requirements with Phase II full-stack requirements
- Added specific technology stack mandates (Next.js, FastAPI, SQLModel, Neon PostgreSQL)
- Included detailed functional requirements for priorities, tags, search, filter, and sort
- Updated project structure to reflect backend/frontend separation
- Maintained Spec-Driven Development principle as non-negotiable
- Added sync impact report documenting the changes made

The constitution now serves as the authoritative document for Phase II development with clear requirements for the full-stack web application.