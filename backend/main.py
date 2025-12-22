import requests
import xml.etree.ElementTree as ET
import trafilatura
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import cohere

# -------------------------------------
# CONFIG
# -------------------------------------
SITEMAP_URL = "https://hibadawood.github.io/Physical-AI-Book/sitemap.xml"
COLLECTION_NAME = "physical-ai-book"

# Cohere API
cohere_client = cohere.Client("lIktbQOgIJ8VjIysFxkM9Bv8AnArRjmh37JdfjEK")
EMBED_MODEL = "embed-english-v3.0"

# Qdrant Cloud
qdrant = QdrantClient(
    
    url="https://8ae780ee-6b71-4de3-a801-458b532f87e9.europe-west3-0.gcp.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.EGpBugNaQP61LYq8IkEROgbCpr_Fa7xg5zeQQFiNQNk" 
)
def get_all_urls(sitemap_url):
    xml = requests.get(sitemap_url).text
    root = ET.fromstring(xml)

    urls = []
    for child in root:
        loc_tag = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc_tag is not None:
            urls.append(loc_tag.text)

    print("\nFOUND URLS:")
    for u in urls:
        print(" -", u)

    return urls


# -------------------------------------
# Step 2 — Download page + extract text
# -------------------------------------
def extract_text_from_url(url):
    html = requests.get(url).text
    text = trafilatura.extract(html)

    if not text:
        print("[WARNING] No text extracted from:", url)

    return text


# -------------------------------------
# Step 3 — Chunk the text
# -------------------------------------
def chunk_text(text, max_chars=1200):
    chunks = []
    while len(text) > max_chars:
        split_pos = text[:max_chars].rfind(". ")
        if split_pos == -1:
            split_pos = max_chars
        chunks.append(text[:split_pos])
        text = text[split_pos:]
    chunks.append(text)
    return chunks


# -------------------------------------
# Step 4 — Create embedding
# -------------------------------------
def embed(text):
    response = cohere_client.embed(
        model=EMBED_MODEL,
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding


# -------------------------------------
# Step 5 — Store in Qdrant
# -------------------------------------
def create_collection():
    print("\nCreating Qdrant collection...")
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
        size=1024,        # Cohere embed-english-v3.0 dimension
        distance=Distance.COSINE
        )
    )

def save_chunk_to_qdrant(chunk, chunk_id, url):
    vector = embed(chunk)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=chunk_id,
                vector=vector,
                payload={
                    "url": url,
                    "text": chunk,
                    "chunk_id": chunk_id
                }
            )
        ]
    )


# -------------------------------------
# MAIN INGESTION PIPELINE
# -------------------------------------
def ingest_book():
    urls = get_all_urls(SITEMAP_URL)

    create_collection()

    global_id = 1

    for url in urls:
        print("\nProcessing:", url)
        text = extract_text_from_url(url)

        if not text:
            continue

        chunks = chunk_text(text)

        for ch in chunks:
            save_chunk_to_qdrant(ch, global_id, url)
            print(f"Saved chunk {global_id}")
            global_id += 1

    print("\n✔️ Ingestion completed!")
    print("Total chunks stored:", global_id - 1)


if __name__ == "__main__":
    ingest_book()


# import os
# import requests
# import xml.etree.ElementTree as ET
# import trafilatura
# from qdrant_client import QdrantClient
# from qdrant_client.models import VectorParams, Distance, PointStruct
# import cohere
# from qdrant_client.http.exceptions import UnexpectedResponse

# # -------------------------------------
# # CONFIG
# # -------------------------------------

# SITEMAP_URL = "https://hibadawood.github.io/Physical-AI-Book/sitemap.xml"
# COLLECTION_NAME = "physical-ai-book"

# COHERE_API_KEY = os.getenv("lIktbQOgIJ8VjIysFxkM9Bv8AnArRjmh37JdfjEK")
# QDRANT_API_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.EGpBugNaQP61LYq8IkEROgbCpr_Fa7xg5zeQQFiNQNk")

# EMBED_MODEL = "embed-english-v3.0"

# # -------------------------------------
# # Clients
# # -------------------------------------

# cohere_client = cohere.Client(COHERE_API_KEY)

# qdrant = QdrantClient(
#     url="https://8ae780ee-6b71-4de3-a801-458b532f87e9.europe-west3-0.gcp.cloud.qdrant.io",
#     api_key=QDRANT_API_KEY,
# )

# # -------------------------------------
# # Step 1 — Extract URLs from sitemap
# # -------------------------------------

# def get_all_urls(sitemap_url):
#     xml = requests.get(sitemap_url).text
#     root = ET.fromstring(xml)

#     urls = []
#     for child in root:
#         loc = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
#         if loc is not None:
#             urls.append(loc.text)

#     print("\nFOUND URLS:")
#     for u in urls:
#         print(" -", u)

#     return urls

# # -------------------------------------
# # Step 2 — Extract page text
# # -------------------------------------

# def extract_text_from_url(url):
#     html = requests.get(url).text
#     text = trafilatura.extract(html)

#     if not text:
#         print("[WARNING] No text extracted:", url)

#     return text

# # -------------------------------------
# # Step 3 — Chunk text
# # -------------------------------------

# def chunk_text(text, max_chars=1200):
#     chunks = []
#     while len(text) > max_chars:
#         split_at = text[:max_chars].rfind(". ")
#         if split_at == -1:
#             split_at = max_chars
#         chunks.append(text[:split_at])
#         text = text[split_at:]
#     chunks.append(text)
#     return chunks

# # -------------------------------------
# # Step 4 — Embeddings
# # -------------------------------------

# def embed(text):
#     res = cohere_client.embed(
#         model=EMBED_MODEL,
#         input_type="search_document",
#         texts=[text],
#     )
#     return res.embeddings[0]

# # -------------------------------------
# # Step 5 — Qdrant
# # -------------------------------------

# def ensure_collection():
#     print("\nEnsuring Qdrant collection exists...")

#     try:
#         qdrant.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=VectorParams(
#                 size=1024,
#                 distance=Distance.COSINE,
#             ),
#         )
#         print("Collection created:", COLLECTION_NAME)

#     except UnexpectedResponse as e:
#         if "already exists" in str(e).lower() or "409" in str(e):
#             print("Collection already exists, continuing...")
#         else:
#             raise e

# def save_chunk(chunk, chunk_id, url):
#     vector = embed(chunk)

#     qdrant.upsert(
#         collection_name=COLLECTION_NAME,
#         points=[
#             PointStruct(
#                 id=chunk_id,
#                 vector=vector,
#                 payload={
#                     "url": url,
#                     "text": chunk,
#                     "chunk_id": chunk_id,
#                 },
#             )
#         ],
#     )

# # -------------------------------------
# # MAIN PIPELINE
# # -------------------------------------

# def ingest_book():
#     urls = get_all_urls(SITEMAP_URL)
#     ensure_collection()

#     global_id = 1

#     for url in urls:
#         print("\nProcessing:", url)
#         text = extract_text_from_url(url)
#         if not text:
#             continue

#         for chunk in chunk_text(text):
#             save_chunk(chunk, global_id, url)
#             print(f"Saved chunk {global_id}")
#             global_id += 1

#     print("\n✅ INGESTION COMPLETE")
#     print("Total chunks:", global_id - 1)

# # -------------------------------------

# if __name__ == "__main__":
#     ingest_book()
