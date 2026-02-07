# Tasks: Todo In-Memory Python Console Application

**Feature**: Todo In-Memory Python Console Application
**Branch**: `001-todo-console-app`
**Generated**: 2025-12-31
**Input**: spec.md, plan.md, research.md, data-model.md

**Note**: This template is filled in by the `/sp.tasks` command. See `.specify/templates/commands/tasks.md` for the execution workflow.

## Implementation Strategy

This document decomposes the approved plan into small, verifiable, non-overlapping tasks that Claude Code can execute without ambiguity. Tasks are organized by user story priority (P1, P2, P3...) to enable independent implementation and testing. Each task follows the checklist format with sequential IDs, story labels, and clear file paths.

**MVP Scope**: User Story 1 (Add Task) - Minimum viable product with core functionality.

## Dependencies

- **Setup Phase** → **Foundational Phase** → **User Story Phases** → **Polish Phase**
- User Story 1 (P1) → No dependencies
- User Story 2 (P1) → Depends on User Story 1 (Task model required)
- User Story 3 (P2) → Depends on User Story 1 (Task model required)
- User Story 4 (P2) → Depends on User Story 1 (Task model required)
- User Story 5 (P1) → Depends on User Story 1 (Task model required)

## Parallel Execution Opportunities

- Task model and service layer can be developed in parallel with CLI interface
- Individual user story implementations can be developed independently after foundational setup
- Documentation tasks can run in parallel with implementation tasks

## Phase 1: Setup

### Goal
Initialize project structure and basic documentation files as specified in the constitution and plan.

### Independent Test Criteria
- Project directory structure matches specification
- Documentation files exist at root level
- UV project initialized successfully

### Tasks

- [X] T001 Initialize Python project with UV enforcing Python 3.13+
- [X] T002 Create required directory structure: src/, specs/, specs/history/
- [X] T003 Create placeholder documentation files: README.md, CLAUDE.md

## Phase 2: Foundational

### Goal
Implement core data models and service layer that will support all user stories.

### Independent Test Criteria
- Task model can be instantiated with required fields
- Task service can manage in-memory task collection
- Sequential ID generation works correctly
- All service methods handle operations without persistence

### Tasks

- [X] T004 [P] Implement Task model in src/models.py with id, title (max 100), description (max 500), completed fields
- [X] T005 [P] Implement TaskService in src/services.py with in-memory storage and sequential ID generation
- [X] T006 [P] Implement TaskService.add_task method with input validation
- [X] T007 [P] Implement TaskService.get_all_tasks method
- [X] T008 [P] Implement TaskService.update_task method with existence checks
- [X] T009 [P] Implement TaskService.delete_task method with existence checks
- [X] T010 [P] Implement TaskService.toggle_task_completion method with existence checks
- [X] T011 [P] Add error handling to TaskService methods for invalid IDs

## Phase 3: User Story 1 - Add New Task (Priority: P1)

### Goal
Enable users to create new tasks with required title and optional description through the menu-driven console interface.

### Independent Test Criteria
- User can select "Add Task" option and provide a title
- New task is created with unique ID and "Incomplete" status
- Task appears in task list immediately after creation
- Title and description are stored correctly

### Tasks

- [X] T012 [US1] Implement Add Task flow in src/cli.py with input validation for title (1-100 chars)
- [X] T013 [US1] Implement description input handling (max 500 chars, optional)
- [X] T014 [US1] Connect CLI Add Task flow to TaskService.add_task method
- [X] T015 [US1] Add error handling for invalid input in Add Task flow
- [X] T016 [US1] Validate that added tasks appear in the task list

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

### Goal
Display all tasks with ID, title, description, and completion status in a readable format through the menu-driven console interface.

### Independent Test Criteria
- All tasks are displayed with ID, title, description, and status
- If no tasks exist, a clear message is shown indicating no tasks exist
- Output is consistent and human-readable

### Tasks

- [X] T017 [US2] Implement View Tasks flow in src/cli.py to display all tasks
- [X] T018 [US2] Format task display with ID, title, description, and completion status
- [X] T019 [US2] Handle case where no tasks exist with appropriate message
- [X] T020 [US2] Connect CLI View Tasks flow to TaskService.get_all_tasks method
- [X] T021 [US2] Ensure output is readable and consistent

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

### Goal
Allow users to modify the title or description of an existing task by providing the task ID through the menu-driven console interface.

### Independent Test Criteria
- User can select "Update Task" and provide a valid task ID
- Task reflects the new information when viewed
- Invalid IDs are handled gracefully without crashing

### Tasks

- [X] T022 [US3] Implement Update Task flow in src/cli.py with task ID validation
- [X] T023 [US3] Handle new title and description input with validation (1-100 chars for title, max 500 for description)
- [X] T024 [US3] Connect CLI Update Task flow to TaskService.update_task method
- [X] T025 [US3] Add error handling for invalid task IDs in Update Task flow
- [X] T026 [US3] Verify updated values are reflected in task list

## Phase 6: User Story 4 - Delete Task (Priority: P2)

### Goal
Remove a task permanently from memory by providing the task ID through the menu-driven console interface.

### Independent Test Criteria
- User can select "Delete Task" and provide a valid task ID
- Deleted task no longer appears in the task list
- Invalid IDs do not crash the app

### Tasks

- [X] T027 [US4] Implement Delete Task flow in src/cli.py with task ID validation
- [X] T028 [US4] Connect CLI Delete Task flow to TaskService.delete_task method
- [X] T029 [US4] Add error handling for invalid task IDs in Delete Task flow
- [X] T030 [US4] Verify deleted task no longer appears in task list
- [X] T031 [US4] Confirm appropriate success message after deletion

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P1)

### Goal
Toggle the completion status of a task to track progress through the menu-driven console interface.

### Independent Test Criteria
- User can select "Mark Complete" or "Mark Incomplete" and provide a valid task ID
- Status updates correctly (Complete/Incomplete)
- Invalid IDs handled safely

### Tasks

- [X] T032 [US5] Implement Mark Complete flow in src/cli.py with task ID validation
- [X] T033 [US5] Implement Mark Incomplete flow in src/cli.py with task ID validation
- [X] T034 [US5] Connect CLI Mark Complete flow to TaskService.toggle_task_completion method
- [X] T035 [US5] Connect CLI Mark Incomplete flow to TaskService.toggle_task_completion method
- [X] T036 [US5] Add error handling for invalid task IDs in toggle flows
- [X] T037 [US5] Verify status changes are immediately visible in task list

## Phase 8: CLI Interface Integration

### Goal
Integrate all user story flows into a unified menu-driven interface.

### Independent Test Criteria
- Main menu displays all required options (Add, View, Update, Delete, Mark Complete/Incomplete, Exit)
- Each menu option routes to the correct functionality
- Application loop functions correctly
- User always knows available actions

### Tasks

- [X] T038 Implement main menu interface in src/cli.py with numbered options (1-7)
- [X] T039 Route menu option 1 to Add Task flow
- [X] T040 Route menu option 2 to View Tasks flow
- [X] T041 Route menu option 3 to Update Task flow
- [X] T042 Route menu option 4 to Delete Task flow
- [X] T043 Route menu option 5 to Mark Complete flow
- [X] T044 Route menu option 6 to Mark Incomplete flow
- [X] T045 Implement Exit functionality for menu option 7
- [X] T046 Add input validation for menu selection (1-7 only)

## Phase 9: Global Error Handling & Stability

### Goal
Ensure the application remains stable under all error conditions and provides clear user feedback.

### Independent Test Criteria
- Invalid inputs never crash the application
- Predictable runtime errors are caught and handled
- Stack traces are not shown to users
- App remains stable under incorrect input

### Tasks

- [X] T047 Implement global error handling for invalid menu selections
- [X] T048 Implement global error handling for non-numeric task IDs
- [X] T049 Add validation for empty or whitespace-only titles
- [X] T050 Suppress stack traces and show user-friendly error messages
- [X] T051 Test error handling with invalid inputs across all flows
- [X] T052 Ensure application continues running after error conditions

## Phase 10: Application Bootstrap

### Goal
Implement the main application entry point that initializes components and starts the user interface loop.

### Independent Test Criteria
- Application starts and exits cleanly
- Menu loop functions correctly
- All components are properly initialized

### Tasks

- [X] T053 Implement application entry point in src/main.py
- [X] T054 Initialize TaskService in main application
- [X] T055 Start main application loop with menu interface
- [X] T056 Route menu selections to appropriate CLI handlers
- [X] T057 Implement graceful exit functionality
- [X] T058 Test complete application flow from start to exit

## Phase 11: Documentation

### Goal
Populate documentation files with project information and usage instructions.

### Independent Test Criteria
- README.md contains project overview, setup, and usage instructions
- CLAUDE.md contains spec-first enforcement rules and coding discipline
- Documentation matches implementation

### Tasks

- [X] T059 Populate README.md with project overview and Python/UV requirements
- [X] T060 Add setup instructions to README.md including "uv run python src/main.py"
- [X] T061 Include example usage in README.md
- [X] T062 Populate CLAUDE.md with spec-first enforcement rules
- [X] T063 Add prohibition of manual coding to CLAUDE.md
- [X] T064 Include prompting discipline and task execution order rules in CLAUDE.md

## Phase 12: Final Verification

### Goal
Validate that all acceptance criteria are met and the application functions as specified.

### Independent Test Criteria
- All five core operations (Add, View, Update, Delete, Mark Complete) function correctly
- IDs are unique per runtime session
- No persistence exists (in-memory only)
- Application runs via UV
- Code structure matches constitution requirements

### Tasks

- [X] T065 Verify Add task works correctly with title and description
- [X] T066 Verify View tasks displays accurate data with proper formatting
- [X] T067 Verify Update task modifies fields correctly
- [X] T068 Verify Delete task removes task from memory
- [X] T069 Verify Mark Complete/Incomplete toggles status correctly
- [X] T070 Confirm IDs are unique per runtime session
- [X] T071 Verify no persistence exists (data lost on restart)
- [X] T072 Test application runs correctly with "uv run python src/main.py"
- [X] T073 Confirm code structure matches constitution requirements
- [X] T074 Perform end-to-end testing of all user workflows
- [X] T075 Final validation that all specification requirements are met