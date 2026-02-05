from sqlmodel import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment, default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app.db")

# Create sync engine for use with sync Session
if DATABASE_URL.startswith("sqlite"):
    # For SQLite
    sync_engine = create_engine(
        DATABASE_URL.replace("+aiosqlite", ""),
        echo=True,
        connect_args={"check_same_thread": False}  # Required for SQLite
    )
else:
    # For PostgreSQL - convert async URL to sync URL for sync engine
    # Add SSL parameters for Neon PostgreSQL
    sync_db_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    # Add SSL mode parameter for Neon
    if "?sslmode=" not in sync_db_url.lower() and "neon" in sync_db_url.lower():
        sync_db_url += "?sslmode=require"
    sync_engine = create_engine(
        sync_db_url,
        echo=True,
        pool_pre_ping=True  # Helps with connection health checks
    )

# Create a sessionmaker that binds to the sync engine
SessionLocal = sessionmaker(bind=sync_engine, class_=Session)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()