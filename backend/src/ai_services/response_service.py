import asyncio
from typing import List, Dict, Any
from uuid import UUID
from openai import AsyncOpenAI
from src.utils.config import settings
from src.models.chat_response import ChatResponseCreate


class ResponseService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate_response(
        self,
        query: str,
        context_list: List[Dict[str, Any]],  # List of content chunks with metadata
        user_query_id: UUID,
        selected_text: str = None
    ) -> ChatResponseCreate:
        """
        Generate a response based on the query and provided context
        """
        # Construct the context for the LLM
        context_str = "\n\n".join([
            f"Content {i+1}:\n{item['text']}"
            for i, item in enumerate(context_list)
        ])
        
        if selected_text:
            # If specific text was selected, prioritize that in the prompt
            prompt = f"""
            Based only on the selected text provided below, please answer the question.
            
            Selected text: {selected_text}
            
            Question: {query}
            
            Please provide a direct answer based only on the selected text. 
            If the selected text doesn't contain the information needed to answer the question, 
            please say so.
            """
        else:
            # General RAG approach using all retrieved context
            prompt = f"""
            Based only on the following context, please answer the question.
            
            Context:
            {context_str}
            
            Question: {query}
            
            Please provide a comprehensive answer based only on the context provided. 
            If the context doesn't contain the information needed to answer the question, 
            please say so. Do not make up information that is not in the context.
            """
        
        # Generate response using OpenAI API
        response = await self.openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system", 
                    "content": "You are an AI assistant for a Physical AI educational book. Answer questions based only on the provided context. Do not make up information."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent, factual responses
            max_tokens=500
        )
        
        # Calculate response time and tokens used (estimated)
        response_text = response.choices[0].message.content
        tokens_used = len(response_text.split())  # Rough estimation
        
        # Create and return the response object
        return ChatResponseCreate(
            user_query_id=user_query_id,
            response_text=response_text,
            source_content_ids=[UUID(item["content_id"]) for item in context_list],
            confidence_score=0.8,  # Placeholder - in a real implementation, this would be calculated
            response_time_ms=500,  # Placeholder - actual timing would be measured
            tokens_used=tokens_used
        )