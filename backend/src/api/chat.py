from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from uuid import UUID
import time
from src.models.user_query import UserQueryCreate
from src.models.chat_response import ChatResponse
from src.services.book_content_service import BookContentService
from src.ai_services.embedding_service import EmbeddingService
from src.ai_services.retrieval_service import RetrievalService
from src.ai_services.response_service import ResponseService
from src.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Initialize services
embedding_service = EmbeddingService()
retrieval_service = RetrievalService(embedding_service)
response_service = ResponseService()


@router.post("/chat/query", response_model=ChatResponse)
async def chat_query(
    query_data: dict,  # Using dict for flexibility
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a query to the RAG chatbot
    """
    query = query_data.get("query", "")
    selected_text = query_data.get("selected_text", None)
    language = query_data.get("language", "en")
    include_sources = query_data.get("include_sources", True)
    
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Measure response time
    start_time = time.time()
    
    try:
        # In a full implementation, we would create a UserQuery record first
        # For now, we'll simulate this with a temporary ID
        user_query_id = UUID(int=0)  # This would be replaced with an actual ID in a full implementation
        
        # Retrieve relevant content based on the query
        if selected_text:
            # If specific text is selected, search in that context
            relevant_contents = await retrieval_service.retrieve_content_from_selection(
                selected_text, db
            )
        else:
            # Otherwise, use the embedding-based retrieval
            search_results = await retrieval_service.retrieve_relevant_content(
                query, max_results=5
            )
            relevant_contents = await retrieval_service.retrieve_content_by_ids(
                [item["content_id"] for item in search_results], db
            )
        
        # Format the context for the response service
        context_list = [
            {
                "content_id": str(content.id),
                "text": content.content,
                "title": content.title
            }
            for content in relevant_contents
        ]
        
        # Generate response using the response service
        chat_response = await response_service.generate_response(
            query=query,
            context_list=context_list,
            user_query_id=user_query_id,
            selected_text=selected_text
        )
        
        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        chat_response.response_time_ms = response_time_ms
        
        # Note: In a complete implementation, we would:
        # 1. Save the UserQuery to the database
        # 2. Save the ChatResponse to the database
        # 3. Link them together properly
        # 4. Return the saved response with a real ID
        
        # For this implementation, we'll return a simulated response
        return ChatResponse(
            id=UUID(int=0),  # Placeholder ID
            user_query_id=user_query_id,
            response_text=chat_response.response_text,
            source_content_ids=chat_response.source_content_ids,
            confidence_score=chat_response.confidence_score,
            response_time_ms=response_time_ms,
            tokens_used=chat_response.tokens_used,
            created_at=None  # Placeholder
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")