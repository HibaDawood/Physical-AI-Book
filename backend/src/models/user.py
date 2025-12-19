from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4
import re


class UserBase(BaseModel):
    email: str
    username: str = Field(..., min_length=3, max_length=30)
    language_preference: str = Field(default="en", regex=r"^[a-z]{2}$")

    @validator('email')
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('Email must be valid')
        return v.lower()

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError('Username can only contain letters, numbers, hyphens, and underscores')
        return v

    @validator('language_preference')
    def validate_language_preference(cls, v):
        # Validate ISO 639-1 language codes
        if len(v) != 2 or not v.isalpha() or not v.islower():
            raise ValueError('Language must be a valid ISO 639-1 code (2 lowercase letters)')
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    language_preference: Optional[str] = Field(None, regex=r"^[a-z]{2}$")


class UserInDB(UserBase):
    id: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    password_hash: str  # This should not be exposed to the API

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    id: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True