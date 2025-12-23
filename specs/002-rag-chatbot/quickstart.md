# Quickstart Guide: RAG-Powered Chatbot for AI Book

## Prerequisites

- Node.js v18+ installed
- Python 3.11+ installed (for content ingestion)
- Access to OpenAI-compatible API (or local embedding model)
- Qdrant Vector Database (cloud or local instance)

## Setup Instructions

### 1. Clone and Navigate to Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Backend Dependencies
```bash
cd backend
npm install
```

### 3. Install Frontend Dependencies
```bash
cd ../book  # or wherever your Docusaurus project is
npm install
```

### 4. Configure Environment Variables
Create a `.env` file in the backend directory with the following:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
EMBEDDING_MODEL=text-embedding-ada-002  # or compatible model
LLM_MODEL=gpt-3.5-turbo  # or compatible model
```

### 5. Ingest Book Content into Vector Database
```bash
cd scripts
node ingest-content.js
```

This script will:
- Read markdown files from the book's `docs/` directory
- Process and chunk the content
- Generate embeddings using the specified model
- Store the content in Qdrant with metadata

## Running the Application

### 1. Start the Backend API Server
```bash
cd backend
python start_api.py
# or alternatively
python -m uvicorn api:app --host 0.0.0.0 --port 8000
```
The backend will start on `http://localhost:8000` by default.

### 2. Run the Docusaurus Frontend
```bash
cd book
npm start
```
The frontend will start on `http://localhost:3000` by default.

### 3. Access the Chatbot
- Navigate to your Docusaurus site
- The chatbot toggle button will appear in the bottom-right corner of all pages
- Click the button to open the chat interface
- Start asking questions about the book content

## API Endpoints

### Chat Endpoint
- **POST** `/api/chat`
- Request body: `{ "message": "your question", "history": [] }`
- Response: `{ "response": "AI answer", "sources": [...] }`

### Health Check
- **GET** `/api/health`
- Response: `{ "status": "healthy", "timestamp": "..." }`

## Troubleshooting

### Common Issues

1. **Chatbot not appearing on pages**:
   - Verify that the SideChatbot component is properly injected in the Layout wrapper
   - Check browser console for any React errors

2. **API connection errors**:
   - Verify backend server is running
   - Check environment variables are correctly set
   - Ensure Qdrant database is accessible

3. **Slow responses**:
   - Check network connectivity to embedding/LM services
   - Verify Qdrant performance for vector search

### Testing the API Directly
You can test the chat endpoint directly using curl:

```bash
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"message": "What is Physical AI?"}'
```

## Development

### Running in Development Mode
For backend development with auto-restart:
```bash
cd backend
npm run dev
```

### Adding New Content
When new book content is added:
1. Run the ingestion script again: `node scripts/ingest-content.js`
2. The new content will be processed and added to the vector database