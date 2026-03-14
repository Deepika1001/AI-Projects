# AI Agent Summary

Last updated: March 14, 2026

## What this project does

The AI agent supports two runtime paths:

- RAG path for knowledge-base questions using Vertex AI Vector Search, Firestore chunk lookup, and Gemini generation
- Tool path for live operational data using locally hosted Spring Boot services for orders, coupons, and users

The main user-facing interface is now a Streamlit chatbot in `ai-agent/streamlit_app.py`.

## Key runtime files

- `ai-agent/streamlit_app.py` - Browser chatbot UI
- `ai-agent/agent.py` - Top-level router used by the chatbot
- `ai-agent/tools.py` - Intent split between RAG and live tool/API routing
- `ai-agent/rag_service.py` - Cloud RAG implementation using Vertex AI + Firestore + Gemini
- `ai-agent/ingestion/build_embeddings.py` - Builds embeddings and writes Vector Search import data
- `ai-agent/ingestion/seed_firestore.py` - Seeds Firestore with sample ecommerce knowledge documents

## Important behavior

- The chatbot replaces the earlier command-line testing flow for normal usage
- RAG questions go through cloud retrieval if configured correctly
- If cloud RAG fails, `agent.py` falls back to the local FAQ answers in `tools.py`
- Tool-style queries such as `where is my order 1` are routed to the local backend services

## Local service routing

Current local service ports used by `tools.py`:

- Order service: `http://localhost:8081`
- User service: `http://localhost:8082`
- Coupon service: `http://localhost:8083`

Current supported natural-language patterns include:

- Order status queries like `where is my order 1`
- Order detail queries like `show order 1`
- Coupon queries like `coupon SAVE10`
- User queries like `show user 1`

## Vector Search and GCP setup

The codebase was updated to stop relying on hardcoded resource IDs. These scripts now use environment variables:

- `ai-agent/create_vector_index.py`
- `ai-agent/deploy_vector_index.py`
- `ai-agent/rag_service.py`
- `ai-agent/test_vector_search.py`

Key environment variables:

- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_CLOUD_LOCATION`
- `VERTEX_VECTOR_DATA_URI`
- `VERTEX_INDEX_RESOURCE_NAME`
- `VERTEX_INDEX_ENDPOINT_RESOURCE_NAME`
- `VERTEX_DEPLOYED_INDEX_ID`
- `VERTEX_INDEX_DISPLAY_NAME`
- `VERTEX_INDEX_ENDPOINT_DISPLAY_NAME`
- `VERTEX_INDEX_DESCRIPTION`
- `VERTEX_EMBEDDING_DIMENSIONS`
- `VERTEX_APPROXIMATE_NEIGHBORS_COUNT`
- `VERTEX_LEAF_NODE_EMBEDDING_COUNT`
- `VERTEX_LEAF_NODES_TO_SEARCH_PERCENT`

## Data export format

The ingestion pipeline was updated to generate the correct Vertex AI import format:

- Output file: `ai-agent/data/rag_chunks.json`
- Format: newline-delimited JSON
- Each record includes:
  - `id`
  - `embedding`
  - `embedding_metadata`

Old generated files such as `rag_chunks.jsonl` were removed.

`ai-agent/data/` is treated as generated output and should not be edited manually.

## Streamlit chatbot

Launch command:

```powershell
.\venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Useful test prompts:

- `What is the return policy?`
- `What payment methods do you support?`
- `Where is my order 1?`
- `Show order 1`
- `Coupon SAVE10`

## Verified GCP resources during this session

These were created and verified on March 14, 2026 and may change later:

- Index: `projects/156917156320/locations/us-central1/indexes/9176535040534773760`
- Endpoint: `projects/156917156320/locations/us-central1/indexEndpoints/6715757648827908096`
- Deployed index ID: `ecommerce_rag_deployed_v2`

If these resources are replaced later, update the related environment variables instead of editing code.

## Known caveats

- Duplicate or conflicting seed data in Firestore can produce cautious Gemini answers
- `test_vertex_ai.py` is older and uses a different auth pattern than the main Vertex-based flow
- Vertex AI SDK deprecation warnings may appear for some model access paths, but the current flow still works

## Recommended startup order

1. Seed Firestore if needed with `ingestion/seed_firestore.py`
2. Build embeddings with `ingestion/build_embeddings.py`
3. Upload `ai-agent/data/rag_chunks.json` to the configured GCS path
4. Create the Vector Search index
5. Deploy the index
6. Start backend services
7. Start the Streamlit chatbot

## What changed in this session

- Added Streamlit chatbot UI
- Merged and improved README architecture visuals
- Switched Vector Search export from `.jsonl` to newline-delimited `.json`
- Replaced `metadata` with `embedding_metadata` for Vertex AI import compatibility
- Removed hardcoded Vertex AI resource IDs in runtime and test scripts
- Added richer Firestore seed data
- Wired tool routing to live local backend APIs for orders, coupons, and users
- Added graceful handling for empty Vector Search results
