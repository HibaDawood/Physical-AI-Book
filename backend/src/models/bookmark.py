from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class ChapterBookmarkBase(BaseModel):
    user_id: UUID
    book_content_id: UUID
    bookmark_notes: Optional[str] = Field(None, max_length=1000)


class ChapterBookmarkCreate(ChapterBookmarkBase):
    pass


class ChapterBookmarkUpdate(BaseModel):
    bookmark_notes: Optional[str] = Field(None, max_length=1000)


class ChapterBookmark(ChapterBookmarkBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True