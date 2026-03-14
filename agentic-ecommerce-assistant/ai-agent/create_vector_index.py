import os
from google.cloud import aiplatform

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "agentic-ecommerce-ai")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
GCS_URI = "gs://agentic-ecommerce-ai/vector_data/"

aiplatform.init(project=PROJECT_ID, location=REGION)

def main():
    """Create a new MatchingEngine tree-approximate-hash vector index.

    This script initializes a Matching Engine index for RAG retrieval.
    """
    index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name="ecommerce-rag-index",
        contents_delta_uri=GCS_URI,
        dimensions=3072,
        approximate_neighbors_count=10,
        distance_measure_type="DOT_PRODUCT_DISTANCE",
        leaf_node_embedding_count=500,
        leaf_nodes_to_search_percent=7,
        description="RAG index for ecommerce knowledge base",
        sync=True,
    )
    print("Index created.")
    print("Resource name:", index.resource_name)

if __name__ == "__main__":
    main()