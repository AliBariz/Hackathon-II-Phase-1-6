---
id: 2
title: "Amend Constitution to Multi-User with Authentication"
stage: constitution
created: 2026-01-07
updated: 2026-01-07
---

# Amend Constitution to Multi-User with Authentication

## PROMPT_TEXT

```
# 📜 Phase II Constitution
## Todo Full-Stack Web Application

---

## 1. Purpose & Scope

This constitution governs **Phase II** of the Todo project.

**Phase I** delivered a **single-user console application**.
**Phase II** transforms that application into a **modern, multi-user, full-stack web application** with authentication, persistent storage, and a spec-driven development workflow.

This document is **binding**.
Any implementation that violates this constitution is considered **invalid**.

---

## 2. Objective

Transform the Phase I console app into a **production-grade web application** that:

- Supports **multiple authenticated users**
- Persists data in a **serverless PostgreSQL database**
- Exposes a **secure REST API**
- Uses a **responsive frontend UI**
- Is built **exclusively through spec-driven, agentic development**

---

## 3. Development Rules (Non-Negotiable)

### 3.1 Agentic Development Only

- Development **must follow** the Agentic Dev Stack:

  **Write Spec → Generate Plan → Break into Tasks → Implement via Claude Code**

- **No manual coding is allowed**
- All implementation must be performed via **Claude Code**
- Evaluation is based on:
  - Specs
  - Prompts
  - Iterations
  - Process discipline (not just output)

---

## 4. Required Features (Basic Level)

All **5 Basic Level features from Phase I** must be implemented as a **web application**, including:

- Task creation
- Task listing
- Task updating
- Task deletion
- Task completion toggling

Additional Phase II requirements:

- Multi-user support
- Authentication & authorization
- Persistent database storage
- RESTful API
- Responsive UI

---

## 5. Locked Technology Stack

This stack is **final and immutable**.

| Layer | Technology |
|-----|-----------|
| Frontend | **Next.js 16+ (App Router)** |
| Backend | **Python FastAPI** |
| ORM | **SQLModel** |
| Database | **Neon Serverless PostgreSQL** |
| Authentication | **Better Auth** |
| Spec-Driven Dev | **Claude Code + Spec-Kit Plus** |

❌ No substitutions
❌ No alternatives
❌ No extra frameworks

---

## 6. Authentication & Security Model

### 6.1 Authentication Provider

- Authentication is handled by **Better Auth**
- Runs on the **Next.js frontend**
- Manages:
  - Signup
  - Signin
  - Sessions

---

### 6.2 Backend Authentication Challenge

The backend is a **separate FastAPI service**, so it cannot rely on frontend session state.

### 6.3 Solution: JWT-Based Authentication

Better Auth **must be configured to issue JWT tokens**.

#### Authentication Flow

1. User logs in on frontend
2. Better Auth issues a **JWT token**
3. Frontend includes token in every API request:

Authorization: Bearer <token>

yaml
Copy code

4. FastAPI backend:
   - Verifies JWT signature
   - Decodes user identity
   - Enforces ownership rules

---

### 6.4 Shared Secret

- Both frontend and backend **must share the same JWT secret**
- Stored as environment variable:

BETTER_AUTH_SECRET

yaml
Copy code

---

### 6.5 Security Guarantees

| Benefit | Description |
|------|------------|
| User Isolation | Users only see their own tasks |
| Stateless Auth | Backend does not call frontend |
| Token Expiry | JWTs expire automatically |
| No Shared DB Session | Services verify auth independently |

---

## 7. REST API Contract

### 7.1 General Rules

- All endpoints:
  - Require a **valid JWT**
  - Return **JSON**
  - Enforce **task ownership**
- Requests without a token return:

401 Unauthorized

yaml
Copy code

---

### 7.2 Endpoints

| Method | Endpoint | Description |
|-----|--------|------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

📌 **Important:**
The backend must **verify that `{user_id}` matches the JWT user ID**.
Mismatch → `403 Forbidden`.

---

## 8. API Behavior After Authentication

- All endpoints require JWT
- Backend extracts user from token
- All queries are filtered by `user_id`
- Task ownership is enforced on:
  - Read
  - Write
  - Update
  - Delete

---

## 9. Monorepo Structure (Spec-Kit + Claude Code)

### 9.1 Repository Layout

hackathon-todo/
├── .spec-kit/
│ └── config.yaml
├── specs/
│ ├── overview.md
│ ├── architecture.md
│ ├── features/
│ │ ├── task-crud.md
│ │ ├── authentication.md
│ │ └── chatbot.md
│ ├── api/
│ │ ├── rest-endpoints.md
│ │ └── mcp-tools.md
│ ├── database/
│ │ └── schema.md
│ └── ui/
│ ├── components.md
│ └── pages.md
├── CLAUDE.md
├── frontend/
│ ├── CLAUDE.md
│ └── (Next.js app)
├── backend/
│ ├── CLAUDE.md
│ └── (FastAPI app)
├── docker-compose.yml
└── README.md

yaml
Copy code

---

## 10. Spec-Kit Configuration

```yaml
# .spec-kit/config.yaml
name: hackathon-todo
version: "1.0"

structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui

phases:
  - name: phase1-console
    features: [task-crud]

  - name: phase2-web
    features: [task-crud, authentication]

  - name: phase3-chatbot
    features: [task-crud, authentication, chatbot]
11. CLAUDE.md Governance
Root CLAUDE.md: project overview, Spec-Kit usage, workflow

frontend/CLAUDE.md: Next.js patterns, UI rules, API client usage

backend/CLAUDE.md: FastAPI structure, SQLModel rules, DB access

Claude Code must obey all CLAUDE.md files.

12. Database Rules
SQLModel is mandatory

Connection via DATABASE_URL

Tasks table includes user_id

All queries must filter by authenticated user

13. Spec-Driven Workflow
Write or update spec in /specs

Reference spec using @specs/...

Ask Claude Code to implement

Claude reads all relevant specs + CLAUDE.md

Claude implements frontend and backend

Iterate only by updating specs

14. Final Principle
Specs are the source of truth.
Claude Code is the executor.
Manual code is forbidden.
```

## RESPONSE_TEXT

Updated the project constitution at `.specify/memory/constitution.md` to reflect the multi-user authentication requirements. The changes included:

- Major version update from 2.0.0 to 3.0.0 due to addition of multi-user authentication and authorization
- Added multi-user support and authentication requirements
- Included Better Auth as mandatory authentication provider
- Added JWT-based authentication flow between frontend and backend
- Defined REST API contract with authentication requirements
- Updated functional requirements to include user_id for task ownership
- Modified project scope to require authenticated access only
- Added user isolation and security model requirements
- Updated repository structure to include .spec-kit configuration
- Added detailed API endpoint specifications with authentication enforcement

The constitution now serves as the authoritative document for multi-user Phase II development with authentication requirements.