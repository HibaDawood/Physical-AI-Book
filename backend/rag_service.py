import os
from dotenv import load_dotenv
from openai import OpenAI
import cohere
from qdrant_client import QdrantClient
from typing import List, Optional
import logging

# --------------------
# Setup logging
# --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------
# Load env
# --------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --------------------
# Validate required environment variables
# --------------------
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is required")
    raise ValueError("GEMINI_API_KEY environment variable is required")

# --------------------
# Gemini (OpenAI compatible)
# --------------------
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# --------------------
# Cohere (Embeddings)
# --------------------
cohere_client = cohere.Client(
    "lIktbQOgIJ8VjIysFxkM9Bv8AnArRjmh37JdfjEK"
)

def get_embedding(text: str):
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text]
    )
    return response.embeddings[0]

# --------------------
# Qdrant
# --------------------
qdrant = QdrantClient(
    url="https://8ae780ee-6b71-4de3-a801-458b532f87e9.europe-west3-0.gcp.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.EGpBugNaQP61LYq8IkEROgbCpr_Fa7xg5zeQQFiNQNk"
)

def retrieve(query: str):
    try:
        embedding = get_embedding(query)
        results = qdrant.query_points(
            collection_name="physical-ai-book",
            query=embedding,
            limit=5
        )
        return [point.payload["text"] for point in results.points]
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return []

# --------------------
# RAG Pipeline with Conversation Context
# --------------------
def answer_question(question: str, conversation_history: Optional[List[dict]] = None):
    try:
        # Retrieve relevant documents based on the current question
        docs = retrieve(question)

        if not docs:
            return "I don't know based on the Physical AI book content."

        # Build context from retrieved documents
        context = "\n\n".join(docs)

        # Build conversation history for context
        history_context = ""
        if conversation_history:
            # Include last 3 exchanges to maintain context without overwhelming the prompt
            recent_history = conversation_history[-3:]
            for msg in recent_history:
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_context += f"{role}: {msg.get('content', '')}\n\n"

        # Construct the prompt with both document context and conversation history
        prompt = f"""
You are an AI tutor for the Physical AI & Humanoid Robotics textbook. Answer questions based on the provided context from the book.

Use ONLY the context below to answer. If the answer is not present in the context, say "I don't know based on the Physical AI book content."

Be conversational and helpful. If the user asks follow-up questions, refer back to your previous answers and the conversation history when relevant.

Context from Physical AI Book:
{context}

Conversation History:
{history_context if history_context else "No previous conversation."}

Question: {question}
"""

        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are an AI tutor for the Physical AI & Humanoid Robotics textbook. Provide accurate, helpful, and concise answers based on the Physical AI book content. Be conversational and acknowledge the user's previous questions when relevant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in answer_question: {e}")
        return "I'm having trouble processing your request right now. Please try again later."