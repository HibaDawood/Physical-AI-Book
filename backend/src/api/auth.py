from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from uuid import UUID
from src.models.user import UserCreate, UserUpdate, UserPublic
from src.utils.config import settings
from src.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # In a real implementation, we would fetch the user from the database
    # For now, we'll just return the user ID
    return UUID(user_id)


@router.post("/auth/register", response_model=UserPublic)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user
    """
    # In a real implementation, we would:
    # 1. Check if user already exists
    # 2. Hash the password
    # 3. Create the user in the database
    
    # Placeholder implementation
    hashed_password = get_password_hash(user.password)
    
    # Return a simulated user object
    return UserPublic(
        id=UUID(int=0),  # Would be real ID in full implementation
        email=user.email,
        username=user.username,
        language_preference=user.language_preference,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@router.post("/auth/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    User login
    """
    # In a real implementation, we would:
    # 1. Fetch user from database by email/username
    # 2. Verify password
    # 3. Create and return JWT token
    
    # Placeholder implementation
    # In a real system, we would verify credentials against the database
    user_id = UUID(int=1)  # Simulated user ID
    access_token = create_access_token(data={"sub": str(user_id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user_id),
            "username": form_data.username
        }
    }


@router.get("/user/profile", response_model=UserPublic)
async def get_user_profile(current_user: UUID = Depends(get_current_user)):
    """
    Get user profile
    """
    # In a real implementation, we would fetch from database
    return UserPublic(
        id=current_user,
        email="user@example.com",  # Placeholder
        username="example_user",  # Placeholder
        language_preference="en",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@router.put("/user/profile", response_model=UserPublic)
async def update_user_profile(
    user_update: UserUpdate, 
    current_user: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user profile
    """
    # In a real implementation, we would update the database
    return UserPublic(
        id=current_user,
        email="user@example.com",  # Placeholder
        username=user_update.username or "example_user",
        language_preference=user_update.language_preference or "en",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )