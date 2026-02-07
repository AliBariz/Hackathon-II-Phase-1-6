# Quickstart Guide: Enhanced Task Management

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL-compatible database (Neon recommended)
- Git for version control

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables:
   - `DATABASE_URL`: Connection string for PostgreSQL database
   - `SECRET_KEY`: Secret key for security
6. Run database migrations: `alembic upgrade head`
7. Start the backend: `uvicorn src.main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Set up environment variables in `.env.local`:
   - `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
4. Start the development server: `npm run dev`

## API Endpoints

### Task Management
- `GET /api/tasks` - Retrieve all tasks with optional query params for filtering/sorting/search
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update an existing task
- `DELETE /api/tasks/{id}` - Delete a task

### Query Parameters for GET /api/tasks
- `search`: Keyword to search in title/description
- `status`: Filter by status (pending/completed)
- `priority`: Filter by priority (high/medium/low)
- `tag`: Filter by tag (work/home)
- `sort`: Sort by (due_date/priority/title)
- `order`: Sort order (asc/desc)

## Running Tests
- Backend: `pytest` in the backend directory
- Frontend: `npm run test` in the frontend directory

## Database Migrations
- Generate migration: `alembic revision --autogenerate -m "migration message"`
- Apply migrations: `alembic upgrade head`