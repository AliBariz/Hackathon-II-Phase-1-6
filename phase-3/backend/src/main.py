import sys
import os
# Add both the current directory and parent directory to sys.path to access routes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from database import engine
from contextlib import asynccontextmanager

# Define lifespan to handle startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    SQLModel.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup can go here if needed

# Create FastAPI app with lifespan
app = FastAPI(
    title="Enhanced Todo API",
    description="Full-stack web application with improved task management featuring priorities, tags, search, filtering, and sorting capabilities.",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003", "http://localhost:3004", "http://localhost:3005"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routes (tasks and search - from the api router but without auth to avoid conflicts)
from api.endpoints import tasks, search
api_router_no_auth = APIRouter()
api_router_no_auth.include_router(tasks.router, prefix="", tags=["tasks"])  # No prefix since paths include user_id
api_router_no_auth.include_router(search.router, prefix="", tags=["search"])  # No prefix since paths include user_id

app.include_router(api_router_no_auth, prefix="/api", tags=["tasks"])

# Also include auth routes directly (not under /api prefix)
from routes import auth
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Enhanced Todo API - Task Management System"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)