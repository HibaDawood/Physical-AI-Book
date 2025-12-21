# API Contracts: Physical AI Book + RAG Chatbot

## Base URL
`https://api.physicalai-book.com/v1`

## Authentication
All API endpoints (except health check) require authentication via Bearer token:
```
Authorization: Bearer {jwt_token}
```

## Endpoints

### Book Content Endpoints

#### GET `/book/contents`
Fetch structured book content based on filters
- **Query Parameters**:
  - `language`: Optional, language code (e.g., "en", "ur")
  - `chapter_number`: Optional, specific chapter to retrieve
  - `parent_id`: Optional, get content under specific parent
- **Response**:
  ```json
  {
    "contents": [
      {
        "id": "uuid",
        "title": "string",
        "content": "text",
        "language": "string",
        "chapter_number": "integer",
        "parent_id": "uuid",
        "metadata": "json_object",
        "created_at": "datetime"
      }
    ],
    "total": "integer",
    "page": "integer",
    "has_more": "boolean"
  }
  ```

#### GET `/book/contents/{content_id}`
Fetch specific content by ID
- **Response**:
  ```json
  {
    "id": "uuid",
    "title": "string",
    "content": "text",
    "language": "string",
    "chapter_number": "integer",
    "parent_id": "uuid",
    "metadata": "json_object",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```

#### GET `/book/chapters`
Get chapter list with hierarchy
- **Response**:
  ```json
  {
    "chapters": [
      {
        "id": "uuid",
        "title": "string",
        "chapter_number": "integer",
        "parent_id": "uuid",
        "has_content": "boolean",
        "children": "[...children]"
      }
    ]
  }
  ```

### RAG Chatbot Endpoints

#### POST `/chat/query`
Submit a query to the RAG chatbot
- **Request Body**:
  ```json
  {
    "query": "string",
    "selected_text": "string",
    "language": "string",
    "include_sources": "boolean"
  }
  ```
- **Response**:
  ```json
  {
    "response_id": "uuid",
    "response_text": "string",
    "confidence_score": "float",
    "sources": [
      {
        "content_id": "uuid",
        "title": "string",
        "excerpt": "string"
      }
    ],
    "response_time_ms": "integer"
  }
  ```
- **Success Codes**:
  - 200: Query processed successfully
  - 400: Invalid query format
  - 429: Rate limit exceeded

### User Management Endpoints

#### POST `/auth/register`
Register a new user
- **Request Body**:
  ```json
  {
    "email": "string",
    "username": "string",
    "password": "string",
    "language_preference": "string"
  }
  ```
- **Response**:
  ```json
  {
    "user_id": "uuid",
    "email": "string",
    "username": "string",
    "access_token": "string",
    "refresh_token": "string"
  }
  ```

#### POST `/auth/login`
User login
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "string",
    "refresh_token": "string",
    "user": {
      "id": "uuid",
      "email": "string",
      "username": "string",
      "language_preference": "string"
    }
  }
  ```

#### GET `/user/profile`
Get user profile
- **Response**:
  ```json
  {
    "id": "uuid",
    "email": "string",
    "username": "string",
    "language_preference": "string",
    "created_at": "datetime"
  }
  ```

#### PUT `/user/profile`
Update user profile
- **Request Body**:
  ```json
  {
    "username": "string",
    "language_preference": "string"
  }
  ```

### Book Interaction Endpoints

#### POST `/user/bookmarks`
Create a bookmark
- **Request Body**:
  ```json
  {
    "book_content_id": "uuid",
    "notes": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": "uuid",
    "book_content_id": "uuid",
    "notes": "string",
    "created_at": "datetime"
  }
  ```

#### GET `/user/bookmarks`
Get user bookmarks
- **Response**:
  ```json
  {
    "bookmarks": [
      {
        "id": "uuid",
        "book_content_id": "uuid",
        "title": "string",
        "notes": "string",
        "created_at": "datetime"
      }
    ]
  }
  ```

#### DELETE `/user/bookmarks/{bookmark_id}`
Delete a bookmark

### Analytics Endpoints

#### POST `/analytics/track`
Track user action
- **Request Body**:
  ```json
  {
    "action_type": "string",
    "action_target": "string",
    "metadata": "json_object"
  }
  ```

### System Endpoints

#### GET `/health`
Health check
- **Response**:
  ```json
  {
    "status": "ok",
    "timestamp": "datetime",
    "services": {
      "database": "ok",
      "vector_db": "ok",
      "storage": "ok"
    }
  }
  ```