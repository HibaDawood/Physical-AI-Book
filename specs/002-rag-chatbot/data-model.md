# Data Model: RAG-Powered Chatbot for AI Book

## Entities

### 1. ChatMessage
**Description**: Represents a single message in the chat conversation
- **id**: String (unique identifier)
- **content**: String (the text content of the message)
- **sender**: String (either "user" or "assistant")
- **timestamp**: DateTime (when the message was created)
- **sources**: Array of SourceReference (optional, for assistant responses)

### 2. SourceReference
**Description**: Reference to the source content that supports an AI response
- **id**: String (unique identifier for the source chunk)
- **title**: String (title of the source document/chapter)
- **url**: String (URL to the source content)
- **content**: String (the actual content that was referenced)
- **similarity_score**: Number (similarity score from vector search)

### 3. QueryRequest
**Description**: Request payload for the chat API
- **message**: String (the user's question)
- **history**: Array of ChatMessage (optional, conversation history)
- **user_id**: String (optional, for tracking purposes)

### 4. QueryResponse
**Description**: Response payload from the chat API
- **response**: String (the AI-generated response)
- **sources**: Array of SourceReference (sources used to generate the response)
- **query_id**: String (unique identifier for the query)

### 5. ContentChunk
**Description**: A chunk of book content stored in the vector database
- **id**: String (unique identifier)
- **content**: String (the text content of the chunk)
- **title**: String (title of the source document)
- **url**: String (URL to the original content)
- **section**: String (section/chapter name)
- **embedding**: Array of Number (vector embedding of the content)
- **metadata**: Object (additional metadata like page number, author, etc.)

## Relationships

### ChatMessage → SourceReference
- A ChatMessage (from assistant) can reference multiple SourceReferences
- This relationship is optional (only for assistant messages)
- Cardinality: One ChatMessage to Many SourceReferences

### QueryResponse → SourceReference
- A QueryResponse can contain multiple SourceReferences
- This represents the sources used to generate the response
- Cardinality: One QueryResponse to Many SourceReferences

### QueryRequest → ChatMessage
- A QueryRequest can include multiple ChatMessage objects in history
- This preserves conversation context
- Cardinality: One QueryRequest to Many ChatMessages

## Validation Rules

### ChatMessage
- `content` must not be empty
- `sender` must be either "user" or "assistant"
- `timestamp` must be a valid date/time

### SourceReference
- `id`, `title`, and `content` must not be empty
- `similarity_score` must be between 0 and 1

### QueryRequest
- `message` must not be empty
- `message` length should be less than 1000 characters

### ContentChunk
- `content`, `title`, and `url` must not be empty
- `embedding` must be a valid array of numbers with consistent dimensions

## State Transitions

### Query Processing States
1. **RECEIVED**: Query is received by the API
2. **RETRIEVING**: Relevant content is being retrieved from vector DB
3. **GENERATING**: LLM is generating the response
4. **COMPLETED**: Response is ready to be returned
5. **FAILED**: Error occurred during processing

## Indexes and Performance Considerations

### ContentChunk
- Vector index on `embedding` field for fast similarity search
- Text index on `title` and `content` for keyword search fallback
- Composite index on `section` and `url` for content organization

### ChatMessage
- Index on `timestamp` for chronological ordering
- Index on `sender` for filtering by user or assistant