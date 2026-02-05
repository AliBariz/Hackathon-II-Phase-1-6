# CLAUDE.md - Todo Full-Stack Web Application

## Project Overview
This is a full-stack todo application with JWT-based authentication using Next.js frontend with Better Auth, FastAPI backend with SQLModel ORM, and Neon PostgreSQL database. The system enforces user isolation by ensuring users can only access their own tasks through JWT token verification and user ID validation in API endpoints.

## Project Structure
- `frontend/` - Next.js application with authentication and task management UI
- `backend/` - FastAPI application with task CRUD endpoints and authentication middleware
- `specs/` - Specification files for features and requirements

## Workflow
1. Write or update spec in `/specs`
2. Reference spec using `@specs/...`
3. Ask Claude Code to implement
4. Claude Code reads:
   - Specs
   - Constitution
   - Relevant CLAUDE.md files
5. Claude implements frontend and backend
6. Changes require spec updates first

## Tech Stack
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI, SQLModel, Pydantic
- Authentication: Better Auth with JWT tokens
- Database: Neon PostgreSQL
- Communication: REST (JSON)

## Development Guidelines
- All code must originate from a specification file
- No manual coding is allowed
- Every feature must be traceable back to a documented specification
- Follow the workflow: Write Specification → Generate Plan → Break Plan into Tasks → Implement via Claude Code → Iterate only through spec updates