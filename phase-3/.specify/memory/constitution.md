<!-- SYNC IMPACT REPORT -->
<!-- Version change: N/A → 1.0.0 -->
<!-- List of modified principles: N/A (initial constitution) -->
<!-- Added sections: All sections (initial creation) -->
<!-- Removed sections: None -->
<!-- Templates requiring updates: N/A (initial creation) -->
<!-- Follow-up TODOs: None -->

# Todo AI Chatbot Constitution
<!-- Phase III Todo Application Constitution -->

## Core Principles

### Agentic Development Only
<!-- I. Strict Spec-Driven Development -->
All development must strictly follow: **Write Spec → Generate Plan → Break into Tasks → Implement via Claude Code**
<!-- Rules: No manual coding, No direct edits outside Claude Code, All changes originate from specs, Evaluation based on specs, plans, tasks, Claude Code prompts and iterations -->

### Locked Technology Stack
<!-- II. Fixed Technology Stack -->
Backend holds **no conversational state**; All state is stored in **database**; MCP tools are **stateless**; AI agent is the **decision-maker**; Backend acts as **orchestrator only**
<!-- Technologies: Frontend: OpenAI ChatKit, Backend: Python FastAPI, AI Framework: OpenAI Agents SDK, MCP Server: Official MCP SDK, ORM: SQLModel, Database: Neon Serverless PostgreSQL, Authentication: Better Auth -->

### Natural Language Task Management
<!-- III. Core Task Operations via Natural Language -->
The chatbot must support all basic task operations via natural language: Add task, List tasks, Update task, Complete task, Delete task
<!-- Each operation must be performed through MCP tools and confirmed with a friendly AI response -->

### Authentication & Authorization
<!-- IV. Strict User Isolation -->
Authentication is handled by **Better Auth**; JWT tokens are required for all chat requests; Backend must verify JWT and extract user_id; Users must only access their own: Tasks, Conversations, Messages
<!-- Enforce user isolation across all data access -->

### MCP Statelessness
<!-- V. Stateless MCP Tools -->
MCP server exposes **task operations as tools**; Tools are **stateless** and persist data via database; Tools **never store memory in process**
<!-- MCP tools must be stateless and rely on database persistence -->

### Spec-Driven Workflow
<!-- VI. Documentation-First Approach -->
All chatbot behavior is defined in `/specs`; Claude Code must reference specs via `@specs/...`; Implementation without spec change is forbidden
<!-- All development originates from specifications -->

## System Architecture
<!-- High-level architecture and database model requirements -->

The system follows a stateless architecture where the backend holds no conversational state, all state is stored in the database, MCP tools are stateless, the AI agent makes decisions, and the backend acts as orchestrator only.

### Database Models
The system requires these database models:
- **Task**: id, user_id, title, description, completed, created_at, updated_at
- **Conversation**: id, user_id, created_at, updated_at
- **Message**: id, conversation_id, user_id, role (user|assistant), content, created_at

## MCP Tools Specification
<!-- Required MCP tools for task operations -->

### add_task
Creates a new task.
Parameters: user_id (string, required), title (string, required), description (string, optional)

### list_tasks
Lists tasks.
Parameters: user_id (string, required), status (optional: all, pending, completed)

### complete_task
Marks task as complete.
Parameters: user_id (string, required), task_id (integer, required)

### delete_task
Deletes a task.
Parameters: user_id (string, required), task_id (integer, required)

### update_task
Updates task title or description.
Parameters: user_id (string, required), task_id (integer, required), title (optional), description (optional)

## Agent Behavior Rules
<!-- Mapping of user intents to actions -->

The AI agent must map user intents to actions:
- Add / remember → `add_task`
- Show / list → `list_tasks`
- Done / finished → `complete_task`
- Delete / remove → `delete_task`
- Change / update → `update_task`

Additional rules:
- Always confirm actions
- Handle missing tasks gracefully
- Ask clarifying questions when ambiguous

## Stateless Conversation Flow
<!-- The 8-step conversation flow process -->

1. Receive user message
2. Fetch conversation history from DB
3. Append new message
4. Run agent with MCP tools
5. Agent invokes tools
6. Persist assistant response
7. Return response
8. Server forgets everything

## Governance
<!-- Constitution governance and amendment procedures -->

This constitution governs Phase III of the Todo project. The AI agent decides, MCP tools act, the server remembers nothing, the database remembers everything.

**Version**: 1.0.0 | **Ratified**: 2026-02-02 | **Last Amended**: 2026-02-02
<!-- Version: 1.0.0 | Ratified: 2026-02-02 | Last Amended: 2026-02-02 -->
