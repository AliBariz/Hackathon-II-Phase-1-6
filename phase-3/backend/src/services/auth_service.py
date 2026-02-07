from typing import Optional
from sqlmodel import Session, select
from models.user import User
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Tuple

# Password hashing context - using multiple schemes for compatibility
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

class AuthService:
    SECRET_KEY = "your-secret-key-change-in-production"  # In production, use environment variable
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        # Limit password length to avoid bcrypt limitations
        truncated_password = password[:72] if len(password) > 72 else password
        return pwd_context.hash(truncated_password)

    @staticmethod
    def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        if not user or not AuthService.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AuthService.SECRET_KEY, algorithm=AuthService.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_user(session: Session, username: str, email: str, password: str) -> Optional[User]:
        # Check if user already exists
        existing_user = session.exec(select(User).where(
            (User.username == username) | (User.email == email)
        )).first()

        if existing_user:
            return None

        # Hash the password
        hashed_password = AuthService.get_password_hash(password)

        # Create new user with hashed password
        db_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_username(session: Session, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()