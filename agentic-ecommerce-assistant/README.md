# Agentic Ecommerce Assistant

## Overview

Agentic Ecommerce Assistant is an end-to-end reference implementation for a conversational AI system in an ecommerce setting. It combines retrieval-augmented generation, domain tool routing, and backend microservices to answer user questions with both indexed knowledge and live operational data.

Core capabilities:

- Vector retrieval using Google Vertex AI Matching Engine
- Semantic embeddings via `gemini-embedding-001`
- Generative responses through `gemini-2.5-flash`
- Firestore as both a knowledge store and transactional store
- Spring Boot microservices for coupons, orders, and users

The assistant uses a RAG pipeline to retrieve relevant context from a chunked knowledge base, then combines that context with Gemini-based answer generation. When a query requires live business data, the agent can call backend services instead of relying only on indexed content.

## Architecture At a Glance

```mermaid
flowchart LR
    A([User])

    subgraph Runtime["Runtime Request Flow"]
      direction LR
      B[Agent Router]
      C[RAG Service]
      D[Tool Dispatcher]
      E[Create Embedding]
      F[Vertex AI Vector Search]
      G[Firestore Chunk Lookup]
      H[Prompt and Context Builder]
      I[Gemini Answer Generation]
      K[Domain Tool APIs]
      Q[Structured Tool Response]

      B -->|RAG route| C
      B -->|Tool route| D
      C --> E
      E --> F
      F --> G
      G --> H
      H --> I
      D --> K
      K --> Q
      Q --> H
    end

    subgraph Backend["Backend Microservices"]
      direction TB
      L1[Coupon Service]
      L2[Order Service]
      L3[User Service]
    end

    subgraph Ingestion["Knowledge Ingestion Pipeline"]
      direction LR
      M[Source Documents]
      N[Chunking and Cleanup]
      O[Embedding Generation]
      P[Index Preparation]

      M --> N
      N --> O
      O --> P
    end

    A -->|User query| B
    I -->|Final answer| A

    K --> L1
    K --> L2
    K --> L3

    L1 -->|Coupon data| Q
    L2 -->|Order data| Q
    L3 -->|User data| Q

    P -. updates vector index .-> F

    classDef user fill:#EAF4FF,stroke:#0B57D0,stroke-width:2px,color:#0F172A;
    classDef runtime fill:#E8F7E8,stroke:#2E7D32,stroke-width:2px,color:#102A12;
    classDef ingestion fill:#FFF4D6,stroke:#C77800,stroke-width:2px,color:#3B2A00;
    classDef backend fill:#F7E8FF,stroke:#7B2CBF,stroke-width:2px,color:#2B1142;

    class A user;
    class B,C,D,E,F,G,H,I,K,Q runtime;
    class M,N,O,P ingestion;
    class L1,L2,L3 backend;
```

### Diagram Notes

- `RAG route` means the query can be answered from indexed knowledge.
- `Tool route` means the assistant needs live operational data from backend services.
- `Structured Tool Response` represents normalized service output before the final answer is composed.
- The dotted arrow from `Index Preparation` to `Vertex AI Vector Search` shows a background update flow, not a per-request runtime call.

### Plain Text Flow

1. A user query enters `ai-agent/agent.py`.
2. The router decides whether to use the RAG pipeline or the tool pipeline.
3. The RAG path performs embedding, vector retrieval, Firestore lookup, prompt construction, and Gemini answer generation.
4. The tool path calls backend services, normalizes their responses, and feeds that data into answer generation.
5. The ingestion pipeline prepares and refreshes the vector index used during retrieval.

---

## Repository Structure

### `ai-agent/`

Python-based RAG service and ingestion utilities.

- `agent.py` - Routes incoming requests across RAG and tool flows.
- `rag_service.py` - Handles retrieval, embeddings, Firestore lookup, and Gemini prompt assembly.
- `create_vector_index.py` - Creates the Vertex AI Matching Engine index.
- `deploy_vector_index.py` - Deploys the vector index for serving.
- `ingestion/` - Chunking and embedding preparation pipeline.
- `tools/` - Domain tool wrappers for coupon, order, and user operations.
- `test_*` - Local tests for RAG behavior.

### `backend/`

Spring Boot microservices for operational data access.

- `coupon-service` - Coupon lookup API such as `/coupons/{code}`
- `order-service` - Order APIs such as `/orders/{id}` and `/orders/{id}/status`
- `user-service` - User APIs such as `/users/register` and `/users/{id}`

### Other directories

- `docs/` - Project documentation
- `frontend/` - Frontend assets and UI work
- `knowledge-base/` - Knowledge content used for ingestion

---

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- Java 17+
- Maven 3.8+
- Google Cloud SDK (`gcloud`) authenticated to your project
- Vertex AI API enabled
- Firestore in Native mode

Recommended environment variables:

- `GOOGLE_CLOUD_PROJECT` - Your Google Cloud project ID
- `GOOGLE_CLOUD_LOCATION` - Deployment region such as `us-central1`

Optional for local testing:

- `GCLOUD_AUTH`

---

## Setup and Run

### AI agent

1. Install Python dependencies:

```bash
cd ai-agent
python -m pip install -r requirements.txt
```

2. Build embeddings from the knowledge base:

```bash
cd ai-agent/ingestion
python build_embeddings.py
```

3. Create and deploy the vector index:

```bash
cd ai-agent
python create_vector_index.py
python deploy_vector_index.py
```

4. Run the RAG interface:

Use your own wrapper around `rag_service.ask_rag(user_query)` or run local test utilities such as `test_rag_local.py`.

### Backend services

Run each microservice separately:

```bash
cd backend/coupon-service
./mvnw spring-boot:run

cd ../order-service
./mvnw spring-boot:run

cd ../user-service
./mvnw spring-boot:run
```

Available API examples:

- `GET /coupons/{code}`
- `GET /orders/{id}`
- `GET /orders/{id}/status`
- `PUT /orders/{id}/address?address=...`
- `POST /users/register`
- `GET /users/{id}`

---

## Implementation Status

Current routing-related structure:

- `ai-agent/agent.py` imports `is_rag_question` and `call_tool` from `ai-agent/tools.py`
- `ai-agent/tools.py` includes:
  - `is_rag_question(user_query)`
  - `ask_rag(user_query)` as a local fallback
  - `call_tool(user_query)` for tool-routing policy
- `ai-agent/rag_service.py` remains the full cloud RAG pipeline path using Vertex AI, Firestore, and Gemini

---

## Documentation and Comments

Documentation has been added in key source files:

- Python: `agent.py`, `create_vector_index.py`, `deploy_vector_index.py`, `rag_service.py`, and ingestion pipeline methods
- Java: controller, service, model, config, and application classes include Javadocs

---

## Testing

### Python

Run from `ai-agent/`:

- `python test_rag_local.py`
- `python test_vector_search.py`

### Java

Run in each backend module:

- `./mvnw test`

---

## Operational Notes

- Seed Firestore collections before testing end-to-end flows. Use `ingestion/seed_firestore.py` or service-specific data loaders where available.
- Replace placeholder endpoints, project IDs, and deployment values with your own environment-specific configuration.
- Keep API keys, service accounts, and cloud credentials secure.
