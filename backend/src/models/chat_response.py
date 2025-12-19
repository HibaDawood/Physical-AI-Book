from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class ChatResponseBase(BaseModel):
    user_query_id: UUID
    response_text: str = Field(..., min_length=1)
    source_content_ids: List[UUID] = []
    confidence_score: float = Field(ge=0.0, le=1.0)
    response_time_ms: int = Field(ge=0)
    tokens_used: int = Field(ge=0)


class ChatResponseCreate(ChatResponseBase):
    pass


class ChatResponseUpdate(BaseModel):
    pass  # No updates needed for responses after creation


class ChatResponse(ChatResponseBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True