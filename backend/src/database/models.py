from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, UUID, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class BookContentDB(Base):
    __tablename__ = "book_contents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    # Note: content_embedding is not stored directly in DB as it's computed from content
    language = Column(String(2), nullable=False, default="en")
    chapter_number = Column(Integer, nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("book_contents.id"), nullable=True)
    metadata = Column(Text, nullable=True)  # Store as JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    children = relationship("BookContentDB", backref="parent")
    user_bookmarks = relationship("ChapterBookmarkDB", back_populates="book_content")


class UserDB(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    language_preference = Column(String(2), nullable=False, default="en")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_sessions = relationship("UserSessionDB", back_populates="user")
    user_queries = relationship("UserQueryDB", back_populates="user")
    chapter_bookmarks = relationship("ChapterBookmarkDB", back_populates="user")
    user_analytics = relationship("UserAnalyticsDB", back_populates="user")


class UserSessionDB(Base):
    __tablename__ = "user_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    ip_address = Column(String(45), nullable=True)  # Support IPv6
    user_agent = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    metadata = Column(Text, nullable=True)  # Store as JSON string

    # Relationships
    user = relationship("UserDB", back_populates="user_sessions")
    user_queries = relationship("UserQueryDB", back_populates="session")


class UserQueryDB(Base):
    __tablename__ = "user_queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Nullable for anonymous users
    query_text = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    language = Column(String(2), nullable=False, default="en")
    session_id = Column(UUID(as_uuid=True), ForeignKey("user_sessions.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("UserDB", back_populates="user_queries")
    session = relationship("UserSessionDB", back_populates="user_queries")
    chat_response = relationship("ChatResponseDB", back_populates="user_query", uselist=False)


class ChatResponseDB(Base):
    __tablename__ = "chat_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_query_id = Column(UUID(as_uuid=True), ForeignKey("user_queries.id"), nullable=False)
    response_text = Column(Text, nullable=False)
    # Store source content IDs as JSON string
    source_content_ids = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    tokens_used = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_query = relationship("UserQueryDB", back_populates="chat_response")


class ChapterBookmarkDB(Base):
    __tablename__ = "chapter_bookmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    book_content_id = Column(UUID(as_uuid=True), ForeignKey("book_contents.id"), nullable=False)
    bookmark_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("UserDB", back_populates="chapter_bookmarks")
    book_content = relationship("BookContentDB", back_populates="user_bookmarks")


class UserAnalyticsDB(Base):
    __tablename__ = "user_analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Nullable for anonymous users
    action_type = Column(String(50), nullable=False)
    action_target = Column(String(255), nullable=False)
    metadata = Column(Text, nullable=True)  # Store as JSON string
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("UserDB", back_populates="user_analytics")