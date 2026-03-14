from google.cloud import firestore
import vertexai
from vertexai.language_models import TextEmbeddingModel
import numpy as np

PROJECT_ID = "agentic-ecommerce-ai"
LOCATION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

embedding_model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")

db = firestore.Client()


def embed_query(query: str):
    embeddings = embedding_model.get_embeddings([query])
    return embeddings[0].values


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_firestore_chunks(query, top_k=3):

    query_embedding = embed_query(query)

    docs = db.collection("knowledge_chunks").stream()

    scored_chunks = []

    for doc in docs:
        data = doc.to_dict()

        similarity = cosine_similarity(
            query_embedding,
            data["embedding"]
        )

        scored_chunks.append({
            "text": data["text"],
            "title": data["title"],
            "score": similarity
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    return scored_chunks[:top_k]


if __name__ == "__main__":

    query = "What is the return policy?"

    results = search_firestore_chunks(query)

    print("\nTop Results:\n")

    for r in results:
        print("Title:", r["title"])
        print("Score:", round(r["score"], 3))
        print("Text:", r["text"])
        print()