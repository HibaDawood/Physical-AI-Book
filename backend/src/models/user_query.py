from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class UserQueryBase(BaseModel):
    query_text: str = Field(..., min_length=1, max_length=2000)
    selected_text: Optional[str] = Field(None, max_length=5000)
    language: str = Field(default="en", regex=r"^[a-z]{2}$")
    session_id: UUID


class UserQueryCreate(UserQueryBase):
    user_id: Optional[UUID] = None


class UserQueryUpdate(BaseModel):
    pass  # No updates needed for queries after creation


class UserQuery(UserQueryBase):
    id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True