# backend/CLAUDE.md - FastAPI Backend for Todo Application

## Overview
This is the backend for the full-stack todo application built with FastAPI. It handles JWT-based authentication, task CRUD operations, and ensures user isolation by validating that users can only access their own tasks.

## Tech Stack
- Framework: FastAPI
- Language: Python 3.11+
- ORM: SQLModel
- Database: Neon PostgreSQL
- Authentication: JWT middleware for token verification
- Validation: Pydantic models for request/response validation

## File Structure
- `main.py` - Application entry point
- `models/` - SQLModel database models
- `schemas/` - Pydantic schemas for request/response validation
- `routes/` - API route definitions
- `services/` - Business logic implementations
- `tests/` - API and integration tests

## Development Guidelines
- All endpoints must require JWT authentication
- Validate that URL user_id parameter matches JWT user ID (enforce user isolation)
- Return proper HTTP status codes: 401 for unauthorized, 403 for forbidden access
- Use Pydantic models for request/response validation
- Implement proper error handling and logging
- Follow SQLModel best practices for database operations

## Authentication & Authorization
- All endpoints require JWT token in Authorization header
- Middleware must verify JWT signature and decode user ID
- Enforce user ownership: user_id in URL must match JWT user ID
- Return 403 Forbidden for mismatched user access attempts
- Return 401 Unauthorized for invalid/missing JWT tokens

## Database Operations
- Use SQLModel for all database interactions
- Ensure proper indexing for performance (especially user_id)
- Implement transaction handling where needed
- Follow FastAPI dependency injection patterns
- Use async database operations where possible

## API Endpoints
- GET /api/{user_id}/tasks - List user's tasks with optional filters
- POST /api/{user_id}/tasks - Create task for user
- GET /api/{user_id}/tasks/{id} - Get specific task
- PUT /api/{user_id}/tasks/{id} - Update specific task
- DELETE /api/{user_id}/tasks/{id} - Delete specific task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion status