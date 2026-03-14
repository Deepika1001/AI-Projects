# rag_service.py

import os
from typing import List, Dict

from google.cloud import firestore
from google.cloud import aiplatform
from google import genai
from google.genai import types

import vertexai
from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput


# =========================
# Config
# =========================
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "agentic-ecommerce-ai")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

ENDPOINT_RESOURCE_NAME = (
    "projects/156917156320/locations/us-central1/indexEndpoints/5379877409359134720"
)
DEPLOYED_INDEX_ID = "ecommerce_rag_deployed"

CHUNKS_COLLECTION = "knowledge_chunks"
EMBEDDING_MODEL_NAME = "gemini-embedding-001"
GEN_MODEL_NAME = "gemini-2.5-flash"


# =========================
# Init clients
# =========================
vertexai.init(project=PROJECT_ID, location=LOCATION)
aiplatform.init(project=PROJECT_ID, location=LOCATION)

db = firestore.Client(project=PROJECT_ID)
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL_NAME)
genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


# =========================
# Embedding
# =========================
def embed_query(query: str) -> List[float]:
    """
    Create query embedding for vector search.
    """
    result = embedding_model.get_embeddings(
        [TextEmbeddingInput(text=query, task_type="RETRIEVAL_QUERY")]
    )
    return result[0].values


# =========================
# Vector Search retrieval
# =========================
def retrieve_neighbor_ids(user_query: str, top_k: int = 3) -> List[str]:
    """
    Query Vertex AI Vector Search and return chunk IDs.
    """
    endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=ENDPOINT_RESOURCE_NAME
    )

    query_embedding = embed_query(user_query)

    response = endpoint.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[query_embedding],
        num_neighbors=top_k,
    )

    neighbor_ids = []
    if response and len(response) > 0:
        for neighbor in response[0]:
            neighbor_ids.append(neighbor.id)

    return neighbor_ids


# =========================
# Firestore chunk lookup
# =========================
def fetch_chunks_by_ids(chunk_ids: List[str]) -> List[Dict]:
    """
    Fetch chunk text/metadata from Firestore knowledge_chunks.
    Keeps result order same as Vector Search ranking.
    """
    if not chunk_ids:
        return []

    chunk_map = {}
    for chunk_id in chunk_ids:
        doc = db.collection(CHUNKS_COLLECTION).document(chunk_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["chunk_id"] = chunk_id
            chunk_map[chunk_id] = data

    ordered_chunks = [chunk_map[cid] for cid in chunk_ids if cid in chunk_map]
    return ordered_chunks


def retrieve_chunks(user_query: str, top_k: int = 3) -> List[Dict]:
    """
    Full retrieval path:
    Vector Search -> chunk IDs -> Firestore chunk documents
    """
    neighbor_ids = retrieve_neighbor_ids(user_query, top_k=top_k)
    return fetch_chunks_by_ids(neighbor_ids)


# =========================
# Prompt assembly
# =========================
def build_context(chunks: List[Dict]) -> str:
    """
    Convert retrieved chunks into a prompt-friendly context block.
    """
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        title = chunk.get("title", "")
        category = chunk.get("category", "")
        source_url = chunk.get("source_url", "")
        text = chunk.get("text", "")

        context_parts.append(
            f"""[Source {i}]
Title: {title}
Category: {category}
Source URL: {source_url}
Content: {text}"""
        )

    return "\n\n".join(context_parts)


# =========================
# Gemini answer generation
# =========================
def ask_gemini_with_context(user_query: str, chunks: List[Dict]) -> str:
    """
    Send retrieved context + user question to Gemini.
    """
    context = build_context(chunks)

    prompt = f"""
You are an ecommerce support assistant.

Rules:
- Answer only using the provided context.
- If the answer is not clearly in the context, say you are not sure.
- Keep the answer concise and helpful.
- If useful, mention the source title in the answer.

Context:
{context}

User question:
{user_query}
"""

    response = genai_client.models.generate_content(
        model=GEN_MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        ),
    )

    return response.text


# =========================
# Public function
# =========================
def ask_rag(user_query: str, top_k: int = 3) -> str:
    """
    Main entry point for RAG-based knowledge questions.
    """
    chunks = retrieve_chunks(user_query, top_k=top_k)

    if not chunks:
        return "I could not find relevant help content for that question."

    return ask_gemini_with_context(user_query, chunks)


# =========================
# Debug helper
# =========================
def debug_retrieval(user_query: str, top_k: int = 3) -> List[Dict]:
    """
    Useful for testing retrieval without Gemini.
    """
    return retrieve_chunks(user_query, top_k=top_k)