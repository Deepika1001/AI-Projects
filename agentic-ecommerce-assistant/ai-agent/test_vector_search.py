import os

import vertexai
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "agentic-ecommerce-ai")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

ENDPOINT_RESOURCE_NAME = os.getenv("VERTEX_INDEX_ENDPOINT_RESOURCE_NAME", "")
DEPLOYED_INDEX_ID = os.getenv("VERTEX_DEPLOYED_INDEX_ID", "ecommerce_rag_deployed")

vertexai.init(project=PROJECT_ID, location=REGION)
aiplatform.init(project=PROJECT_ID, location=REGION)

embedding_model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")


def embed_query(query):
    embeddings = embedding_model.get_embeddings(
        [TextEmbeddingInput(text=query, task_type="RETRIEVAL_QUERY")]
    )
    return embeddings[0].values


if not ENDPOINT_RESOURCE_NAME:
    raise ValueError("Missing VERTEX_INDEX_ENDPOINT_RESOURCE_NAME environment variable.")

endpoint = aiplatform.MatchingEngineIndexEndpoint(
    index_endpoint_name=ENDPOINT_RESOURCE_NAME
)

query = "What is the return policy?"

query_embedding = embed_query(query)

response = endpoint.find_neighbors(
    deployed_index_id=DEPLOYED_INDEX_ID,
    queries=[query_embedding],
    num_neighbors=3,
)

print("\nTop Vector Matches:\n")

if not response or not response[0]:
    print("No vector matches returned.")
    print("Check that:")
    print("- rag_chunks.json was uploaded to the configured GCS vector_data path")
    print("- the uploaded file uses the expected newline-delimited JSON format")
    print("- the index was created after the correct file was uploaded")
    print("- the deployed index contains imported embeddings")
else:
    for neighbor in response[0]:
        print("Chunk ID:", neighbor.id)
        print("Distance:", neighbor.distance)
        print("---------------------------")
