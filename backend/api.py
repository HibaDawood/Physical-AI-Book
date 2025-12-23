from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from rag_service import answer_question, retrieve

# --------------------
# FastAPI App
# --------------------
app = FastAPI(
    title="Physical AI Book RAG API",
    description="API for interacting with the Physical AI Book using Retrieval Augmented Generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []

class QueryRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []

@app.get("/")
def read_root():
    return {"message": "Physical AI Book RAG API"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    try:
        # Get the answer from the RAG pipeline with conversation history
        answer = answer_question(chat_request.message, chat_request.history)

        # Retrieve sources for the response
        sources = retrieve(chat_request.message)

        return ChatResponse(response=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_endpoint(query_request: QueryRequest):
    """Simple query endpoint that returns just the answer"""
    try:
        answer = answer_question(query_request.query)
        sources = retrieve(query_request.query)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)