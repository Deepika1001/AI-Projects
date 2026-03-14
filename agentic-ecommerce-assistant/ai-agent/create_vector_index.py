import os
from google.cloud import aiplatform

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "agentic-ecommerce-ai")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
GCS_URI = os.getenv("VERTEX_VECTOR_DATA_URI", "")
INDEX_DISPLAY_NAME = os.getenv("VERTEX_INDEX_DISPLAY_NAME", "ecommerce-rag-index")
INDEX_DESCRIPTION = os.getenv(
    "VERTEX_INDEX_DESCRIPTION",
    "RAG index for ecommerce knowledge base",
)
EMBEDDING_DIMENSIONS = int(os.getenv("VERTEX_EMBEDDING_DIMENSIONS", "3072"))
APPROXIMATE_NEIGHBORS_COUNT = int(os.getenv("VERTEX_APPROXIMATE_NEIGHBORS_COUNT", "10"))
LEAF_NODE_EMBEDDING_COUNT = int(os.getenv("VERTEX_LEAF_NODE_EMBEDDING_COUNT", "500"))
LEAF_NODES_TO_SEARCH_PERCENT = int(os.getenv("VERTEX_LEAF_NODES_TO_SEARCH_PERCENT", "7"))

aiplatform.init(project=PROJECT_ID, location=REGION)

def main():
    """Create a new MatchingEngine tree-approximate-hash vector index.

    This script initializes a Matching Engine index for RAG retrieval.
    """
    if not GCS_URI:
        raise ValueError("Missing VERTEX_VECTOR_DATA_URI environment variable.")

    index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name=INDEX_DISPLAY_NAME,
        contents_delta_uri=GCS_URI,
        dimensions=EMBEDDING_DIMENSIONS,
        approximate_neighbors_count=APPROXIMATE_NEIGHBORS_COUNT,
        distance_measure_type="DOT_PRODUCT_DISTANCE",
        leaf_node_embedding_count=LEAF_NODE_EMBEDDING_COUNT,
        leaf_nodes_to_search_percent=LEAF_NODES_TO_SEARCH_PERCENT,
        description=INDEX_DESCRIPTION,
        sync=True,
    )
    print("Index created.")
    print("Resource name:", index.resource_name)

if __name__ == "__main__":
    main()
