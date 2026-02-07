from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
from database import sync_engine  # Import the sync engine from database.py

# Load environment variables
load_dotenv()

# Get database URL from environment, default to SQLite for local dev
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app.db")

# Create async engine based on database type
if DATABASE_URL.startswith("sqlite"):
    # For SQLite
    async_engine = create_async_engine(
        DATABASE_URL,
        poolclass=StaticPool,  # SQLite works better with StaticPool
        echo=True,
        connect_args={"check_same_thread": False}  # Required for SQLite
    )
else:
    # For PostgreSQL - ensure we use the asyncpg driver
    postgresql_async_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    async_engine = create_async_engine(
        postgresql_async_url,
        echo=True
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup using the sync engine
    SQLModel.metadata.create_all(bind=sync_engine)
    yield
    # Cleanup on shutdown

app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003", "http://localhost:3004", "http://localhost:3005", "http://localhost:3006", "http://localhost:3007", "http://localhost:3008", "http://localhost:3009"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

# Include routes
from routes import tasks
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])

# Also include auth routes
from routes import auth
app.include_router(auth.router)

# Include chat endpoint
from chat_endpoint_simple import router as chat_router
app.include_router(chat_router)