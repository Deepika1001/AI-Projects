import os
from google.cloud import aiplatform
from google.cloud import aiplatform_v1

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "agentic-ecommerce-ai")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
INDEX_RESOURCE_NAME = os.getenv("VERTEX_INDEX_RESOURCE_NAME", "")
DEPLOYED_INDEX_ID = os.getenv("VERTEX_DEPLOYED_INDEX_ID", "ecommerce_rag_deployed")
ENDPOINT_DISPLAY_NAME = os.getenv("VERTEX_INDEX_ENDPOINT_DISPLAY_NAME", "ecommerce-rag-endpoint")

aiplatform.init(project=PROJECT_ID, location=REGION)

def main():
    """Deploy an existing Matching Engine index to a public endpoint."""
    if not INDEX_RESOURCE_NAME:
        raise ValueError("Missing VERTEX_INDEX_RESOURCE_NAME environment variable.")

    index = aiplatform.MatchingEngineIndex(INDEX_RESOURCE_NAME)

    # Use the GAPIC client to create the endpoint and wait for the long-running
    # operation result. This avoids the intermittent helper-path 404 that can
    # happen when the higher-level SDK re-reads the endpoint immediately.
    client = aiplatform_v1.IndexEndpointServiceClient(
        client_options={"api_endpoint": f"{REGION}-aiplatform.googleapis.com"}
    )
    parent = f"projects/{PROJECT_ID}/locations/{REGION}"
    create_op = client.create_index_endpoint(
        parent=parent,
        index_endpoint=aiplatform_v1.IndexEndpoint(
            display_name=ENDPOINT_DISPLAY_NAME,
            public_endpoint_enabled=True,
        ),
    )
    created_endpoint = create_op.result()

    endpoint = aiplatform.MatchingEngineIndexEndpoint(created_endpoint.name)

    endpoint.deploy_index(
        index=index,
        deployed_index_id=DEPLOYED_INDEX_ID,
        sync=True,
    )

    print("Endpoint created and index deployed.")
    print("Endpoint resource name:", endpoint.resource_name)

if __name__ == "__main__":
    main()
