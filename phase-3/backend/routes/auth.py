from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
import re
from passlib.context import CryptContext

from services.auth import AuthService
from models.user import User
from sqlmodel import Session, select
from database import get_session  # We'll need to create this

# Password hashing context - use argon2 as it's more reliable than bcrypt
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])

# Request models
class UserRegisterRequest(BaseModel):
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

# Response models
class AuthResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    message: str

class UserResponse(BaseModel):
    id: str
    email: str

# Helper function for password validation
def validate_password(password: str) -> bool:
    # At least 8 characters, one uppercase, one lowercase, one number
    # Also ensure it's not longer than 72 characters for bcrypt compatibility
    if len(password) < 8:
        return False
    if len(password) > 72:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

# Helper function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to hash password
def get_password_hash(password: str) -> str:
    # Truncate password to 72 characters if longer (bcrypt limitation)
    # This should not happen due to validation, but as a safety measure
    safe_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(safe_password)

# Registration endpoint
@router.post("/register", response_model=AuthResponse)
async def register(user_data: UserRegisterRequest, session: Session = Depends(get_session)):
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password strength
    if not validate_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number"
        )

    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Hash the password
    password_hash = get_password_hash(user_data.password)

    # Create the new user
    user = User(email=user_data.email, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create and return a token
    token_data = {"sub": user.id, "email": user.email}
    token = AuthService.create_access_token(
        data=token_data,
        expires_delta=timedelta(hours=24)  # Token valid for 24 hours
    )

    return AuthResponse(
        success=True,
        token=token,
        message="User registered successfully"
    )

# Login endpoint
@router.post("/login", response_model=AuthResponse)
async def login(user_data: UserLoginRequest, session: Session = Depends(get_session)):
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Find the user by email
    user = session.exec(select(User).where(User.email == user_data.email)).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create and return a token
    token_data = {"sub": user.id, "email": user.email}
    token = AuthService.create_access_token(
        data=token_data,
        expires_delta=timedelta(hours=24)  # Token valid for 24 hours
    )

    return AuthResponse(
        success=True,
        token=token,
        message="Login successful"
    )

# Logout endpoint (client-side token removal is sufficient)
@router.post("/logout", response_model=AuthResponse)
async def logout():
    return AuthResponse(
        success=True,
        message="Logout successful"
    )

# Get current user endpoint
@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: dict = Depends(AuthService.get_current_user)):
    # In a real implementation, we'd fetch user details from the database
    # Using the user ID from the token
    return UserResponse(
        id=current_user.get("sub", ""),
        email=current_user.get("email", "")
    )