import os
from google.cloud import aiplatform

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "156917156320")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
INDEX_RESOURCE_NAME = "projects/156917156320/locations/us-central1/indexes/6845077808440410112"

aiplatform.init(project=PROJECT_ID, location=REGION)

def main():
    index = aiplatform.MatchingEngineIndex(INDEX_RESOURCE_NAME)

    endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
        display_name="ecommerce-rag-endpoint",
        public_endpoint_enabled=True,
        sync=True,
    )

    endpoint.deploy_index(
        index=index,
        deployed_index_id="ecommerce_rag_deployed",
        sync=True,
    )

    print("Endpoint created and index deployed.")
    print("Endpoint resource name:", endpoint.resource_name)

if __name__ == "__main__":
    main()