import vertexai
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput

PROJECT_ID = "156917156320"
REGION = "us-central1"

ENDPOINT_RESOURCE_NAME = "projects/156917156320/locations/us-central1/indexEndpoints/5379877409359134720"
DEPLOYED_INDEX_ID = "ecommerce_rag_deployed"

vertexai.init(project=PROJECT_ID, location=REGION)
aiplatform.init(project=PROJECT_ID, location=REGION)

embedding_model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")


def embed_query(query):
    embeddings = embedding_model.get_embeddings(
        [TextEmbeddingInput(text=query, task_type="RETRIEVAL_QUERY")]
    )
    return embeddings[0].values


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

for neighbor in response[0]:
    print("Chunk ID:", neighbor.id)
    print("Distance:", neighbor.distance)
    print("---------------------------")