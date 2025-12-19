import asyncio
from typing import List
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from uuid import UUID
from src.utils.config import settings


class EmbeddingService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.qdrant_client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=True
        )
        self.collection_name = "book_content_embeddings"

    async def initialize_collection(self):
        """Initialize the Qdrant collection for storing embeddings"""
        try:
            # Check if collection exists
            await self.qdrant_client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            await self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),  # OpenAI embedding size
            )

    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a given text using OpenAI API"""
        response = await self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"  # Using OpenAI's embedding model
        )
        return response.data[0].embedding

    async def store_embedding(self, content_id: UUID, content_text: str, metadata: dict = None):
        """Store embedding in Qdrant with content ID as payload"""
        embedding = await self.create_embedding(content_text)
        
        await self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=str(content_id),
                    vector=embedding,
                    payload={
                        "content_id": str(content_id),
                        "text": content_text,
                        **(metadata or {})
                    }
                )
            ]
        )

    async def search_similar(self, query: str, limit: int = 5) -> List[dict]:
        """Search for similar content based on query"""
        query_embedding = await self.create_embedding(query)
        
        search_results = await self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True
        )
        
        return [
            {
                "content_id": UUID(result.payload["content_id"]),
                "text": result.payload["text"],
                "similarity": result.score
            }
            for result in search_results
        ]

    async def delete_embedding(self, content_id: UUID):
        """Delete embedding from Qdrant"""
        await self.qdrant_client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[str(content_id)]
            )
        )

    async def update_embedding(self, content_id: UUID, new_content_text: str, metadata: dict = None):
        """Update an existing embedding"""
        await self.delete_embedding(content_id)
        await self.store_embedding(content_id, new_content_text, metadata)