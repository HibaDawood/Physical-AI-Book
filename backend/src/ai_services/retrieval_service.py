from typing import List, Dict, Any
from uuid import UUID
from src.ai_services.embedding_service import EmbeddingService
from src.services.book_content_service import BookContentService
from src.models.book_content import BookContent


class RetrievalService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service

    async def retrieve_relevant_content(
        self, 
        query: str, 
        user_id: UUID = None,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant content chunks based on the query
        """
        # Search for similar content using embeddings
        search_results = await self.embedding_service.search_similar(
            query, limit=max_results
        )
        
        # Return the search results with content IDs and similarity scores
        return [
            {
                "content_id": result["content_id"],
                "text": result["text"],
                "similarity": result["similarity"]
            }
            for result in search_results
        ]

    async def retrieve_content_by_ids(
        self,
        content_ids: List[UUID],
        db
    ) -> List[BookContent]:
        """
        Retrieve specific content by their IDs
        """
        contents = []
        for content_id in content_ids:
            content = await BookContentService.get_book_content(db, content_id)
            if content:
                contents.append(content)
        return contents

    async def retrieve_content_from_selection(
        self,
        selected_text: str,
        db
    ) -> List[BookContent]:
        """
        Retrieve content that contains the selected text
        """
        # This is a simplified approach - in practice, you might want to 
        # use more sophisticated text matching techniques
        all_contents = await BookContentService.get_book_contents(db, skip=0, limit=1000)
        matching_contents = [
            content for content in all_contents 
            if selected_text.lower() in content.content.lower()
        ]
        return matching_contents[:5]  # Return top 5 matches