import os
from dotenv import load_dotenv
from openai import OpenAI
import cohere
from qdrant_client import QdrantClient

# --------------------
# Load env
# --------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
    embedding = get_embedding(query)
    results = qdrant.query_points(
        collection_name="physical-ai-book",
        query=embedding,
        limit=5
    )
    return [point.payload["text"] for point in results.points]

# --------------------
# RAG Pipeline
# --------------------
def answer_question(question: str):
    docs = retrieve(question)

    if not docs:
        return "I don't know"

    context = "\n\n".join(docs)

    prompt = f"""
You are an AI tutor for the Physical AI & Humanoid Robotics textbook.

Use ONLY the context below to answer.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# --------------------
# Run
# --------------------
if __name__ == "__main__":
    question = "what is physical ai?"
    answer = answer_question(question)
    print("\nANSWER:\n", answer)
