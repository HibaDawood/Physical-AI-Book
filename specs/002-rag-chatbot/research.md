# Research: RAG-Powered Chatbot for AI Book

## Decision: Technology Stack Selection
**Rationale**: The technology stack is based on the feature requirements and constraints:
- Frontend: Docusaurus (React) - already existing in the project
- Backend: Node.js (Express) - matches requirements
- Vector Database: Qdrant - specified in constraints
- Embeddings: OpenAI-compatible API - specified in requirements

## Alternatives Considered:
1. Using Python FastAPI backend instead of Node.js - rejected because requirements specify Node.js
2. Using different vector database (Pinecone, Weaviate) - rejected because Qdrant is specified
3. Using iframe approach - rejected because constraints specify "No iframe chatbot"

## Decision: Content Ingestion Strategy
**Rationale**: Extract markdown content from the existing docs/ directory and convert to embeddings for RAG system.
- Process: docs/*.md → clean markdown → chunk text → generate embeddings → store in Qdrant
- Chunk size: 500-800 tokens with 100-token overlap to maintain context
- Metadata: Include title, section, and URL for proper citations

## Alternatives Considered:
1. Converting to HTML first - rejected because markdown is cleaner for content extraction
2. Different chunk sizes - 500-800 tokens is optimal for context and performance

## Decision: Chat Interface Positioning
**Rationale**: Implement as a floating component in the bottom-right corner of all pages.
- Approach: Create React component that can be injected into the Docusaurus layout
- Toggle mechanism: Fixed position with open/close state
- Responsive: Works on mobile and desktop with appropriate sizing

## Decision: RAG Implementation Architecture
**Rationale**: Three-tier architecture for optimal performance and maintainability:
1. Content Ingestion Layer: Processes markdown files and creates embeddings
2. API Layer: Handles queries, retrieves relevant content, and generates responses
3. UI Layer: Provides user interface for asking questions and viewing responses

## Alternatives Considered:
1. Client-side RAG - rejected for security and performance reasons
2. Direct database queries from frontend - rejected for security reasons

## Decision: Embedding Model Selection
**Rationale**: Use OpenAI-compatible embedding API as specified in requirements.
- Model: OpenAI text-embedding-ada-002 or compatible
- For local deployment: Sentence transformers as alternative
- Consistent embedding dimensions for Qdrant compatibility

## Decision: LLM Selection for Response Generation
**Rationale**: Use OpenAI-compatible API for response generation as specified.
- Primary: OpenAI GPT models
- Alternative: Local models (e.g., Llama) for offline capability
- System prompt designed to ensure RAG compliance and prevent hallucination

## Decision: Security and Rate Limiting
**Rationale**: Implement rate limiting and input sanitization for production readiness.
- Rate limiting: Prevent abuse of the API
- Input sanitization: Prevent injection attacks
- API keys in environment variables: Secure access to external services

## Best Practices Researched:
1. **React Component Design**: Floating action button pattern for chat interface
2. **RAG Architecture**: Proper separation of retrieval and generation components
3. **Docusaurus Integration**: Using theme components for global injection
4. **Qdrant Usage**: Optimal vector search parameters for content retrieval
5. **Markdown Processing**: Libraries like remark and rehype for content extraction
6. **Error Handling**: Graceful degradation when services are unavailable
7. **Accessibility**: Proper ARIA labels and keyboard navigation support