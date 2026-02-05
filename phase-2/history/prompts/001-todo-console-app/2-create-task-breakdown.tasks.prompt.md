---
id: 2
title: Create Task Breakdown
stage: tasks
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-console-app
branch: 001-todo-console-app
user: AGICO
command: sp.tasks
labels: [tasks,spec-driven,implementation]
links:
  spec: specs/001-todo-console-app/spec.md
  plan: specs/001-todo-console-app/plan.md
  tasks: specs/001-todo-console-app/tasks.md
  adr: null
  pr: null
files:
 - specs/001-todo-console-app/tasks.md
tests:
---

## Prompt

```text
# 📄 003-task-breakdown.md
## Spec-Kit Plus – Atomic Task Breakdown
**Todo In-Memory Python Console Application (Phase I)**

---

## 1. Task Breakdown Metadata

- **Task Document ID:** 003
- **Derived From:**
  - `constitution.md`
  - `001-initial-spec.md`
  - `002-plan.md`
- **Methodology:** Spec-Kit Plus
- **Execution Agent:** Claude Code
- **Manual Coding:** Forbidden
- **Granularity Level:** Atomic, deterministic, sequential

This document decomposes the approved plan into **small, verifiable, non-overlapping tasks** that Claude Code can execute without ambiguity.

---

## 2. Execution Rules (Binding)

- Tasks **must be executed in order**
- Each task must be **fully completed and validated** before moving to the next
- No task may introduce behavior not defined in the spec
- Any ambiguity requires **spec clarification**, not assumptions
- Code must remain traceable:
  **Task → Plan → Spec → Constitution**

---

## 3. Phase 1 – Foundation Setup

### T1. Initialize Project with UV
- Initialize Python project using `uv`
- Enforce Python version **3.13+**
- Ensure project runs in a virtual environment
- No dependencies added unless explicitly required

**Output:**
- UV-managed project initialized successfully

---

### T2. Create Directory Structure
Create the following directories exactly as defined:

src/
specs/
specs/history/

yaml
Copy code

**Validation:**
- No extra directories
- No missing directories

---

### T3. Create Required Documentation Files
Create empty or placeholder files:

- `README.md`
- `CLAUDE.md`

**Validation:**
- Files exist at project root
- No application logic inside these files

---

## 4. Phase 2 – Core Domain Modeling

### T4. Define Task Model (`src/models.py`)
- Create `Task` data structure
- Fields:
  - `id: int`
  - `title: str` (max 100 chars)
  - `description: str | None` (max 500 chars)
  - `completed: bool`
- Default `completed = False`

**Constraints:**
- No business logic
- No input/output
- No validation beyond initialization

**Validation:**
- Task object can be instantiated correctly

---

## 5. Phase 3 – Business Logic Layer

### T5. Implement Task Service (`src/services.py`)
Create a service responsible for managing tasks in memory.

**Responsibilities:**
- Maintain an in-memory list of tasks
- Generate sequential unique IDs per runtime
- Enforce existence checks

**Required Methods:**
- `add_task(title, description)`
- `get_all_tasks()`
- `update_task(task_id, title=None, description=None)`
- `delete_task(task_id)`
- `toggle_task_completion(task_id)`

**Constraints:**
- No user input/output
- No persistence
- Graceful handling of invalid IDs

**Validation:**
- All methods behave according to spec
- Invalid IDs do not crash the service

---

## 6. Phase 4 – CLI Interaction Layer

### T6. Design Menu-Driven Interface (`src/cli.py`)
- Display numbered menu options:
  1. Add Task
  2. View Tasks
  3. Update Task
  4. Delete Task
  5. Mark Complete / Incomplete
  6. Exit

**Validation:**
- Menu is readable and consistent
- User always knows available actions

---

### T7. Implement Input Validation Logic
- Validate numeric menu input
- Validate task ID input
- Enforce input length limits:
  - Title ≤ 100 characters
  - Description ≤ 500 characters
- Reject empty or whitespace-only titles

**Constraints:**
- No crashes from invalid input
- Clear, human-readable error messages

---

### T8. Implement CLI Flows
For each menu option, implement a dedicated flow:

- Add task flow
- View tasks flow
- Update task flow
- Delete task flow
- Toggle completion flow

**Constraints:**
- No business logic inside CLI
- Delegate all operations to service layer

**Validation:**
- Each flow correctly triggers service methods
- Output reflects actual task state

---

## 7. Phase 5 – Application Bootstrap

### T9. Implement Application Entry Point (`src/main.py`)
- Initialize task service
- Start main application loop
- Route menu selections to CLI handlers
- Handle graceful exit

**Constraints:**
- No direct task manipulation
- No complex logic

**Validation:**
- Application starts and exits cleanly
- Menu loop functions correctly

---

## 8. Phase 6 – Error Handling & Stability

### T10. Global Error Handling
- Ensure invalid inputs never crash the application
- Catch and handle predictable runtime errors
- Suppress stack traces from user output

**Validation:**
- App remains stable under incorrect input

---

## 9. Phase 7 – Documentation Generation

### T11. Populate README.md
Include:
- Project overview
- Python & UV requirements
- Setup instructions
- Run command:
uv run python src/main.py

yaml
Copy code
- Example usage

---

### T12. Populate CLAUDE.md
Include:
- Spec-first enforcement rules
- Prohibition of manual coding
- Prompting discipline
- Task execution order rules

---

## 10. Phase 8 – Final Verification

### T13. Acceptance Validation
Verify all acceptance criteria:

- ✅ Add task works correctly
- ✅ View tasks displays accurate data
- ✅ Update task modifies fields
- ✅ Delete task removes task
- ✅ Toggle completion works
- ✅ IDs unique per runtime
- ✅ No persistence exists
- ✅ App runs via UV
- ✅ Code structure matches constitution

---

## 11. Completion Rule

The project is considered **complete** only when:
- All tasks T1–T13 are executed successfully
- No deviations from spec, plan, or constitution exist
- No manual code edits are present

**End of Task Breakdown 003**
```

## Response snapshot

Created the complete task breakdown for the Todo In-Memory Python Console Application at specs/001-todo-console-app/tasks.md with 75 specific, actionable tasks organized across 12 phases:

- Phase 1: Setup (3 tasks) - Project initialization and basic documentation
- Phase 2: Foundational (11 tasks) - Core data models and service layer
- Phase 3: User Story 1 - Add New Task (5 tasks) - P1 priority feature
- Phase 4: User Story 2 - View All Tasks (5 tasks) - P1 priority feature
- Phase 5: User Story 3 - Update Task Details (5 tasks) - P2 priority feature
- Phase 6: User Story 4 - Delete Task (5 tasks) - P2 priority feature
- Phase 7: User Story 5 - Mark Task Complete/Incomplete (6 tasks) - P1 priority feature
- Phase 8: CLI Interface Integration (8 tasks) - Menu-driven interface
- Phase 9: Global Error Handling & Stability (6 tasks) - Error handling and stability
- Phase 10: Application Bootstrap (6 tasks) - Main application entry point
- Phase 11: Documentation (6 tasks) - README and CLAUDE documentation
- Phase 12: Final Verification (11 tasks) - Complete validation and testing

All tasks follow the required checklist format with sequential IDs, story labels where appropriate, and specific file paths.

## Outcome

- ✅ Impact: Created comprehensive task breakdown for Todo Console App implementation
- 🧪 Tests: No tests needed for task creation
- 📁 Files: Created tasks.md with 75 specific tasks across 12 phases
- 🔁 Next prompts: Ready for implementation with /sp.implement
- 🧠 Reflection: Tasks are organized by user story priority and follow spec-driven approach

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A