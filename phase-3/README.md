# Todo Full-Stack Web Application

A full-stack todo application with JWT-based authentication using Next.js frontend with Better Auth, FastAPI backend with SQLModel ORM, and Neon PostgreSQL database. The system enforces user isolation by ensuring users can only access their own tasks through JWT token verification and user ID validation in API endpoints.

## Features

- **User Authentication**: JWT-based authentication with Better Auth
- **Task Management**: Create, read, update, delete, and complete tasks
- **User Isolation**: Users can only access their own tasks
- **Search & Filter**: Search and filter tasks by various criteria
- **Priority Management**: Tasks with low/medium/high priority levels
- **Responsive UI**: Works on desktop and mobile devices

## Tech Stack

- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI, SQLModel, Pydantic
- **Authentication**: Better Auth with JWT tokens
- **Database**: Neon PostgreSQL
- **Communication**: REST API with JSON

## Architecture

The application follows a clean separation between frontend and backend:

- `frontend/` - Next.js application with authentication and task management UI
- `backend/` - FastAPI application with task CRUD endpoints and authentication middleware
- `specs/` - Specification files for features and requirements

## Setup Instructions

### Prerequisites

- Node.js 18+ for frontend
- Python 3.11+ for backend
- Neon PostgreSQL database instance

### Environment Variables

#### Backend
```bash
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname"
BETTER_AUTH_SECRET="your-secret-key-here"
```

#### Frontend
```bash
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000/api/auth"
```

### Backend Setup

```bash
cd backend
pip install fastapi uvicorn sqlmodel python-jose python-multipart
```

### Frontend Setup

```bash
cd frontend
npm install next react react-dom @better-auth/react @better-auth/client axios
```

### Running the Application

#### Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm run dev
```

## API Endpoints

All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

### Available Endpoints

- `GET /api/{user_id}/tasks` - List all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task for a user
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task for a user
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task for a user
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Security

- JWT-based authentication between frontend and backend
- User isolation - users can only access their own tasks
- Proper validation of user_id in URL against JWT user ID
- Secure password hashing and storage
- Audit logging for sensitive operations

## Development

This project follows a spec-driven development workflow:

1. Write or update spec in `/specs`
2. Reference spec using `@specs/...`
3. Ask Claude Code to implement
4. Claude Code reads specs, constitution, and relevant CLAUDE.md files
5. Claude implements frontend and backend
6. Changes require spec updates first

## License

[Specify license as needed]