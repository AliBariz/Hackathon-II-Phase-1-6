# Quickstart Guide: User Authentication with JWT

## Prerequisites

- Node.js 18+ for Next.js frontend
- Python 3.11+ for FastAPI backend
- Neon PostgreSQL database instance
- Better Auth account configured

## Environment Setup

### Backend Environment Variables
```bash
# Database
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname"

# Authentication
BETTER_AUTH_SECRET="your-secret-key-here"
BETTER_AUTH_URL="http://localhost:3000"  # Frontend URL
```

### Frontend Environment Variables
```bash
# Backend API
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000/api/auth"
```

## Initial Setup Commands

### Backend Setup
```bash
cd backend
pip install fastapi uvicorn sqlmodel python-jose python-multipart
pip install -r requirements.txt  # if exists
```

### Frontend Setup
```bash
cd frontend
npm install next react react-dom @better-auth/react @better-auth/client
npm install axios  # for API client
```

## Running the Application

### Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend (Next.js)
```bash
cd frontend
npm run dev
```

## Key Integration Points

### 1. JWT Token Flow
1. User logs in via Better Auth on frontend
2. Better Auth issues JWT token
3. Frontend stores token and attaches to API requests
4. Backend verifies JWT signature and extracts user ID
5. Backend validates user_id in URL matches JWT user ID

### 2. API Authentication
All API requests must include:
```http
Authorization: Bearer <jwt-token>
```

### 3. User Isolation
- Backend checks that `user_id` in URL path matches user ID in JWT
- Requests with mismatched user_id return 403 Forbidden
- Requests without valid JWT return 401 Unauthorized

## Testing Authentication Flow

1. Start both backend and frontend
2. Navigate to frontend and register/login
3. Create a task and verify it's associated with your user_id
4. Try to access another user's tasks (should fail with 403)
5. Verify JWT expiration handling

## Common Issues

- **401 Unauthorized**: JWT token missing or invalid
- **403 Forbidden**: User ID in URL doesn't match JWT user ID
- **Database Connection**: Verify DATABASE_URL is correct
- **JWT Secret Mismatch**: Ensure same secret in frontend and backend