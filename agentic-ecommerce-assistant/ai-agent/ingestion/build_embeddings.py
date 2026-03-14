# ingestion/build_embeddings.py

import json
import os
import re
from datetime import datetime, timezone
from typing import Dict, List

from google.cloud import firestore
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


# =========================
# Config
# =========================
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "agentic-ecommerce-ai")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

SOURCE_COLLECTION = "knowledge_base"
CHUNKS_COLLECTION = "knowledge_chunks"

OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "rag_chunks.jsonl")

EMBEDDING_MODEL_NAME = "gemini-embedding-001"

# Chunking settings
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

# Firestore batch size for writes
BATCH_SIZE = 200


# =========================
# Clients
# =========================
db = firestore.Client(project=PROJECT_ID)
vertexai.init(project=PROJECT_ID, location=LOCATION)
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL_NAME)


# =========================
# Helpers
# =========================
def normalize_text(text: str) -> str:
    """Clean whitespace and normalize text before chunking."""
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Simple character-based chunking with overlap.
    Good enough for first implementation.
    """
    text = normalize_text(text)
    if not text:
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_len:
            break

        start = max(end - overlap, 0)

    return chunks


def fetch_active_knowledge_docs() -> List[Dict]:
    """Read active source docs from Firestore knowledge_base."""
    docs = (
        db.collection(SOURCE_COLLECTION)
        .where("is_active", "==", True)
        .stream()
    )

    results = []
    for doc in docs:
        data = doc.to_dict()
        data["doc_id"] = doc.id
        results.append(data)

    return results


def build_chunk_records(source_docs: List[Dict]) -> List[Dict]:
    """Convert source docs into chunk records."""
    chunk_records: List[Dict] = []

    for doc in source_docs:
        content = doc.get("content", "")
        if not content:
            continue

        chunks = chunk_text(content)

        for idx, chunk in enumerate(chunks):
            chunk_id = f"{doc['doc_id']}_chunk_{idx:03d}"

            chunk_records.append(
                {
                    "chunk_id": chunk_id,
                    "doc_id": doc["doc_id"],
                    "title": doc.get("title", ""),
                    "category": doc.get("category", "general"),
                    "source_url": doc.get("source_url", ""),
                    "text": chunk,
                    "chunk_index": idx,
                    "is_active": True,
                    "updated_at": datetime.now(timezone.utc),
                }
            )

    return chunk_records


def embed_document_text(text: str) -> List[float]:
    """
    Create an embedding for a document chunk.
    For retrieval pipelines, document chunks should use the RETRIEVAL_DOCUMENT task type.
    """
    text_input = TextEmbeddingInput(
        text=text,
        task_type="RETRIEVAL_DOCUMENT",
    )
    result = embedding_model.get_embeddings([text_input])
    return result[0].values


def attach_embeddings(chunk_records: List[Dict]) -> List[Dict]:
    """Generate embeddings for every chunk."""
    embedded_records = []

    for i, record in enumerate(chunk_records, start=1):
        embedding = embed_document_text(record["text"])
        record_with_embedding = dict(record)
        record_with_embedding["embedding"] = embedding
        embedded_records.append(record_with_embedding)

        if i % 10 == 0:
            print(f"Embedded {i}/{len(chunk_records)} chunks...")

    return embedded_records


def clear_existing_chunks_for_docs(doc_ids: List[str]) -> None:
    """
    Deletes old chunk docs for the source docs being rebuilt.
    Keeps Firestore clean when you rerun ingestion.
    """
    if not doc_ids:
        return

    # Firestore "in" filter supports limited values, so chunk into groups.
    group_size = 10
    for i in range(0, len(doc_ids), group_size):
        group = doc_ids[i:i + group_size]
        docs = db.collection(CHUNKS_COLLECTION).where("doc_id", "in", group).stream()

        batch = db.batch()
        count = 0

        for doc in docs:
            batch.delete(doc.reference)
            count += 1

            if count % BATCH_SIZE == 0:
                batch.commit()
                batch = db.batch()

        if count % BATCH_SIZE != 0:
            batch.commit()


def save_chunks_to_firestore(records: List[Dict]) -> None:
    """Save chunk metadata + embedding into Firestore knowledge_chunks."""
    batch = db.batch()
    count = 0

    for record in records:
        doc_ref = db.collection(CHUNKS_COLLECTION).document(record["chunk_id"])

        firestore_doc = {
            "chunk_id": record["chunk_id"],
            "doc_id": record["doc_id"],
            "title": record["title"],
            "category": record["category"],
            "source_url": record["source_url"],
            "text": record["text"],
            "chunk_index": record["chunk_index"],
            "embedding": record["embedding"],  # optional but handy for debugging
            "embedding_model": EMBEDDING_MODEL_NAME,
            "embedding_dimension": len(record["embedding"]),
            "is_active": record["is_active"],
            "updated_at": record["updated_at"],
        }

        batch.set(doc_ref, firestore_doc)
        count += 1

        if count % BATCH_SIZE == 0:
            batch.commit()
            batch = db.batch()

    if count % BATCH_SIZE != 0:
        batch.commit()

    print(f"Saved {count} chunks to Firestore collection '{CHUNKS_COLLECTION}'.")


def write_jsonl_for_vector_search(records: List[Dict], output_file: str = OUTPUT_FILE) -> None:
    """
    Write JSONL in a simple Vector Search-friendly format.
    Each line contains:
      - id
      - embedding
      - metadata
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for record in records:
            item = {
                "id": record["chunk_id"],
                "embedding": record["embedding"],
                "metadata": {
                    "doc_id": record["doc_id"],
                    "title": record["title"],
                    "category": record["category"],
                    "source_url": record["source_url"],
                    "chunk_index": record["chunk_index"],
                    "text": record["text"],
                },
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Wrote {len(records)} records to {output_file}")


def main() -> None:
    print("Fetching active knowledge docs from Firestore...")
    source_docs = fetch_active_knowledge_docs()

    if not source_docs:
        print("No active documents found in knowledge_base.")
        return

    print(f"Found {len(source_docs)} source docs.")

    print("Building chunks...")
    chunk_records = build_chunk_records(source_docs)

    if not chunk_records:
        print("No chunks created. Check your source document content.")
        return

    print(f"Built {len(chunk_records)} chunks.")

    print("Deleting old chunks for these docs...")
    doc_ids = [doc["doc_id"] for doc in source_docs]
    clear_existing_chunks_for_docs(doc_ids)

    print("Generating embeddings...")
    embedded_records = attach_embeddings(chunk_records)

    # Sanity check
    first_dim = len(embedded_records[0]["embedding"])
    print(f"Embedding dimension: {first_dim}")

    print("Saving chunk metadata to Firestore...")
    save_chunks_to_firestore(embedded_records)

    print("Writing JSONL for Vector Search...")
    write_jsonl_for_vector_search(embedded_records)

    print("Done.")


if __name__ == "__main__":
    main()