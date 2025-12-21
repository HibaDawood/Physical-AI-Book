# Data Model: Physical AI Book + RAG Chatbot

## Core Entities

### BookContent
- **id**: UUID, Primary Key
- **title**: String, Book/chapter title
- **content**: Text, Main content of the book/chapter
- **content_embedding**: Vector, Embedding vector for RAG search (not stored directly, computed from content)
- **language**: String, Language code (en, ur, etc.)
- **chapter_number**: Integer, Order of chapter in book
- **parent_id**: UUID, Foreign Key to parent chapter/section (null for top level)
- **metadata**: JSON, Additional metadata about the content
- **created_at**: DateTime, Creation timestamp
- **updated_at**: DateTime, Last update timestamp

### User
- **id**: UUID, Primary Key
- **email**: String, User's email address
- **username**: String, User's chosen username
- **password_hash**: String, Hashed password
- **language_preference**: String, Preferred language (en, ur, etc.)
- **is_active**: Boolean, Whether account is active
- **created_at**: DateTime, Account creation timestamp
- **updated_at**: DateTime, Last profile update timestamp

### UserSession
- **id**: UUID, Primary Key
- **user_id**: UUID, Foreign Key to User
- **session_token**: String, Session identifier
- **ip_address**: String, User's IP address
- **user_agent**: Text, User agent string
- **started_at**: DateTime, Session start time
- **ended_at**: DateTime, Session end time (null if active)
- **metadata**: JSON, Additional session metadata

### UserQuery
- **id**: UUID, Primary Key
- **user_id**: UUID, Foreign Key to User (nullable for anonymous users)
- **query_text**: Text, Original user query
- **selected_text**: Text, Specific text selected by user if using "answer from selected text"
- **language**: String, Language of query
- **session_id**: UUID, Foreign Key to UserSession
- **created_at**: DateTime, Query timestamp

### ChatResponse
- **id**: UUID, Primary Key
- **user_query_id**: UUID, Foreign Key to UserQuery
- **response_text**: Text, Chatbot's response
- **source_content_ids**: Array[UUID], IDs of content used as source for response
- **confidence_score**: Float, Confidence level of response (0-1)
- **response_time_ms**: Integer, Time taken to generate response
- **created_at**: DateTime, Response timestamp
- **tokens_used**: Integer, Number of tokens used in response

### ChapterBookmark
- **id**: UUID, Primary Key
- **user_id**: UUID, Foreign Key to User
- **book_content_id**: UUID, Foreign Key to BookContent
- **bookmark_notes**: Text, User's notes on the bookmark
- **created_at**: DateTime, Bookmark creation timestamp
- **updated_at**: DateTime, Last update timestamp

### UserAnalytics
- **id**: UUID, Primary Key
- **user_id**: UUID, Foreign Key to User (nullable for anonymous)
- **action_type**: String, Type of action (page_view, chat_query, book_interaction, etc.)
- **action_target**: String, Target of action (page_url, chapter_id, etc.)
- **metadata**: JSON, Additional action-specific metadata
- **timestamp**: DateTime, When action occurred

## Relationships

1. **User** 1 -> * **UserSession**: Users can have multiple sessions
2. **UserSession** 1 -> * **UserQuery**: Sessions contain multiple queries
3. **UserQuery** 1 -> 1 **ChatResponse**: Each query generates one response
4. **ChatResponse** * -> * **BookContent**: Responses can reference multiple content items
5. **User** 1 -> * **ChapterBookmark**: Users can bookmark multiple content items
6. **User** 1 -> * **UserAnalytics**: Users generate multiple analytics events
7. **BookContent** 1 -> * **BookContent**: Parent-child relationship for hierarchical content

## Validation Rules

1. **BookContent**:
   - Title must not be empty
   - Content must be at least 50 characters when present
   - Language must be a valid ISO language code
   - Chapter number must be non-negative

2. **User**:
   - Email must be valid email format
   - Username must be 3-30 characters
   - Password must meet complexity requirements
   - Language preference must be supported

3. **UserQuery**:
   - Query text must not be empty
   - Selected text, if present, must be from the same book

4. **ChatResponse**:
   - Response text must not be empty
   - Confidence score must be between 0 and 1
   - Tokens used must be positive

## State Transitions (if applicable)

1. **UserSession**:
   - ACTIVE (default) -> ENDED (when session completes)

2. **BookContent**:
   - DRAFT -> PUBLISHED (when content is ready for users)