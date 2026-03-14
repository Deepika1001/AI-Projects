# Agentic Ecommerce Assistant

## Overview

Agentic Ecommerce Assistant is an end-to-end reference implementation for a conversational AI system in an ecommerce context. It combines:

- Vector retrieval using Google Vertex AI Matching Engine (RAG)
- Semantic embeddings via `gemini-embedding-001`
- Generative answers through `gemini-2.5-flash`
- Firestore as a knowledge store and transactional store for coupons, orders, users
- Microservices for coupons, orders, and users in Spring Boot (Java)

The agent uses a RAG pipeline to retrieve related content from a chunked knowledge base and then summarization/generation by Gemini.

---

## Repository Structure

- `ai-agent/` - Python-based RAG service and ingestion utilities.
  - `agent.py` - Routing across RAG and tools.
  - `rag_service.py` - Retrieval, embeddings, Firestore lookup, Gemini prompt assembly.
  - `create_vector_index.py`, `deploy_vector_index.py` - Vertex AI Matching Engine index lifecycle.
  - `ingestion/` - Chunking and embedding data preparation pipeline.
  - `tools/` - Domain tool wrappers (coupons, orders, user). 
  - `test_*` - Local tests for RAG behaviors.

- `backend/` - Three microservices:
  - `coupon-service` - Coupon lookup API `/coupons/{code}`.
  - `order-service` - Order operations API `/orders/{id}` etc.
  - `user-service` - User operations API `/users` endpoints.

- `docs/`, `frontend/`, `knowledge-base/` - project docs, front-end artifacts, and KB content.

---

## Prerequisites

- Python 3.10+
- Java 17+
- Maven 3.8+
- Google Cloud SDK (`gcloud`) authenticated to your project
- Vertex AI API enabled, Firestore in native mode, and GPU quotas if needed.

Environment variables:

- `GOOGLE_CLOUD_PROJECT` - GCP project ID.
- `GOOGLE_CLOUD_LOCATION` - Region (e.g., `us-central1`).

Optional for testing:

- `GCLOUD_AUTH` etc.

---

## AI-Agent Setup and Run

1. Install Python dependencies:

```bash
cd ai-agent
python -m pip install -r requirements.txt
```

2. Prepare knowledge base and embeddings:

```bash
cd ai-agent/ingestion
python build_embeddings.py
``` 

3. Create and deploy DA vector index:

```bash
cd ai-agent
python create_vector_index.py
python deploy_vector_index.py
```

4. Run the RAG service (interface):

Run your own wrapper to call `rag_service.ask_rag(user_query)` or use `test_rag_local.py`.

---

## Backend Services

Build and run each service separately:

```bash
cd backend/coupon-service
./mvnw spring-boot:run

cd ../order-service
./mvnw spring-boot:run

cd ../user-service
./mvnw spring-boot:run
```

APIs:
- `GET /coupons/{code}`
- `GET /orders/{id}`
- `GET /orders/{id}/status`
- `PUT /orders/{id}/address?address=...`
- `POST /users/register`
- `GET /users/{id}`

---

## Comments Added to Code

I have added method-level and class-level documentation in source files:

- Python: `agent.py`, `create_vector_index.py`, `deploy_vector_index.py`, `rag_service.py` has built-in docs, and ingestion pipeline methods are documented.
- Java: all controller/service/model/config and application files now contain Javadocs.

---

## Testing

- Python tests within `ai-agent`:
  - `python test_rag_local.py`
  - `python test_vector_search.py`

- Java tests for microservices:
  - `./mvnw test` in each backend module.

---

## Architecture Flow Diagram

### Mermaid diagram (GitHub + compatible viewers)

```mermaid
flowchart LR
    A[User Query] --> B[Agent Router (ai-agent/agent.py)]
    B -->|RAG question| C[RAG Service (ai-agent/rag_service.py)]
    B -->|Tool call| D[Tool Dispatcher (ai-agent/tools/*.py)]

    C --> E[Embedding (gemini-embedding-001, Vertex AI)]
    E --> F[Vector Search (Matching Engine Index)]
    F --> G[Firestore Chunks Lookup (knowledge_chunks)]
    G --> H[Context Builder + Prompt Assembly]
    H --> I[Gemini Generation (gemini-2.5-flash)]
    I --> J[Answer to User]

    D --> K[Domain Tool APIs]
    K --> L[Backend Microservices]

    subgraph Backend Services
      L1[Coupon Service (Spring Boot + Firestore)]
      L2[Order Service (Spring Boot + Firestore)]
      L3[User Service (Spring Boot + Firestore)]
    end

    K --> L1
    K --> L2
    K --> L3

    subgraph Ingestion
      M[Text & PDF Content] --> N[Chunking & Cleanup (ai-agent/ingestion/build_embeddings.py)]
      N --> O[Embedding & Firestore Save]
      O --> P[JSONL for Indexing]
      P --> F
    end
```

### Plain text fallback (always visible)

1. User query arrives at `ai-agent/agent.py`
2. Route to RAG service or tool dispatcher.
3. RAG path: embed → vector search → Firestore chunk retrieval → prompt → Gemini generate.
4. Tool path: route to domain-specific backend (coupon/order/user services).
5. Ingestion path: source docs → chunking → embedding → Firestore save → JSONL index.

---

## Notes

- Ensure Firestore collections are seeded (use `ingestion/seed_firestore.py` or service-specific data loaders).
- In production, replace placeholder endpoint and project IDs with your values.
- Keep API keys and service accounts secure.
