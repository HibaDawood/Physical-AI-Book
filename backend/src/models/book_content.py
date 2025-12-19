from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4


class BookContentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=50)
    language: str = Field(default="en", regex=r"^[a-z]{2}$")
    chapter_number: int = Field(ge=0)
    parent_id: Optional[UUID] = None
    metadata: Optional[dict] = {}

    @validator('language')
    def validate_language(cls, v):
        # Validate ISO 639-1 language codes
        if len(v) != 2 or not v.isalpha() or not v.islower():
            raise ValueError('Language must be a valid ISO 639-1 code (2 lowercase letters)')
        return v

    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()


class BookContentCreate(BookContentBase):
    pass


class BookContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = Field(None, min_length=50)
    language: Optional[str] = Field(None, regex=r"^[a-z]{2}$")
    chapter_number: Optional[int] = Field(None, ge=0)
    parent_id: Optional[UUID] = None
    metadata: Optional[dict] = None


class BookContent(BookContentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    content_embedding: Optional[List[float]] = None

    class Config:
        from_attributes = True