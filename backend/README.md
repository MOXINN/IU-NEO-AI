# IU NWEO AI — Backend

> FastAPI + LangGraph Agentic RAG system powering the Integral University AI Assistant.

## Architecture

```
backend/
├── main.py                          # App factory (lifespan, CORS, routes)
├── app/
│   ├── core/                        # Framework infrastructure
│   │   ├── config.py                # Pydantic Settings (.env loading)
│   │   ├── database.py              # Async PostgreSQL pool (psycopg v3)
│   │   ├── errors.py                # Custom exception hierarchy
│   │   ├── middleware.py            # Global error handler + request logging
│   │   └── lifespan.py             # Startup/shutdown lifecycle
│   ├── models/                      # Pydantic DTOs (request/response)
│   │   ├── chat.py                  # ChatRequest, ChatStreamEvent
│   │   └── health.py               # HealthResponse, ServiceStatus
│   ├── services/                    # Business logic layer
│   │   ├── chat_service.py          # Chat orchestration (fast-path + LangGraph)
│   │   └── health_service.py        # Dependency health checks
│   ├── api/                         # Thin route handlers (controllers)
│   │   ├── dependencies.py          # FastAPI DI functions
│   │   └── routes/
│   │       ├── chat.py              # POST /api/v1/chat/stream
│   │       └── health.py           # GET  /api/v1/health
│   └── ai/                          # ML/AI pipeline (separated from web layer)
│       ├── models/gemini.py         # Gemini LLM factory
│       ├── graph/                   # LangGraph orchestration
│       │   ├── state.py             # AgentState TypedDict
│       │   ├── builder.py           # StateGraph construction
│       │   └── nodes/               # Pipeline nodes
│       │       ├── classify.py      # Intent classification
│       │       ├── vector_search.py # ChromaDB retrieval
│       │       ├── graph_search.py  # Neo4j retrieval
│       │       ├── generate.py      # Response generation
│       │       └── fallback.py      # Safe fallback
│       ├── rag/                     # RAG store clients
│       │   ├── vector_store.py      # ChromaDB client
│       │   ├── graph_store.py       # Neo4j client
│       │   └── document_loader.py   # Document chunking
│       └── routing/
│           └── semantic_router.py   # FastEmbed instant matching
├── scripts/
│   ├── ingest_documents.py          # ChromaDB seeder
│   └── seed_neo4j.py               # Neo4j graph seeder
├── tests/
│   ├── conftest.py                  # Test fixtures
│   ├── test_health.py               # Health endpoint tests
│   ├── test_chat.py                 # Chat/SSE tests
│   └── test_graph_pipeline.py       # LangGraph node tests
└── data/sample/                     # Reserved for real university documents
```

## Prerequisites

- **Python** 3.11+
- **Docker** & Docker Compose (for databases)
- **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)

## Environment Setup

1. Copy the example env file:
   ```bash
   cp .env.example .env
   ```

2. Fill in your values in `.env`:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   DATABASE_URL=postgresql://iu_user:iu_password@localhost:5432/iu_langgraph
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=iu_neo4j_pass
   CHROMA_HOST=localhost
   CHROMA_PORT=8000
   APP_DEBUG=true
   CORS_ORIGINS=["http://localhost:3000"]
   ```

## Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running

### Option 1: Local Development (with Docker databases)

```bash
# Start databases only
cd ..
docker compose up -d postgres neo4j chroma

# Run the backend with hot-reload
cd backend
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Option 2: Full Docker Stack

```bash
cd ..
docker compose up -d
```

## Database Seeding

Before using RAG features, seed the databases:

```bash
# Seed ChromaDB with university documents
python -m scripts.ingest_documents

# Seed Neo4j with course/prerequisite graph
python -m scripts.seed_neo4j
```

## API Reference

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | Service info (name, version, status) | None |
| `GET` | `/api/v1/health` | Health check for all services | None |
| `POST` | `/api/v1/chat/stream` | SSE chat stream | None |
| `GET` | `/docs` | Swagger UI (debug mode only) | None |
| `GET` | `/redoc` | ReDoc docs (debug mode only) | None |

### POST `/api/v1/chat/stream`

**Request Body:**
```json
{
  "message": "What are the prerequisites for Machine Learning?",
  "thread_id": "thread_abc123"
}
```

**SSE Events:**
| Event | Data | Description |
|-------|------|-------------|
| `status` | `"Classifying query..."` | Pipeline stage transition |
| `message` | `"Machine Learning requires..."` | Token chunk from LLM |
| `done` | `"[DONE]"` | Stream completed |
| `error` | `"Error description"` | Stream error |

### GET `/api/v1/health`

**Response:**
```json
{
  "status": "operational",
  "services": {
    "postgres": "ok",
    "chroma": "ok",
    "neo4j": "unavailable",
    "semantic_router": "ok"
  }
}
```

## LangGraph Pipeline

```
START → classify_intent → route_intent
  ├─ academic/admin/greeting (≥0.6 confidence) → vector_search → generate → END
  ├─ prerequisite (≥0.6 confidence)            → graph_search  → generate → END
  └─ unknown / low confidence                  → fallback      → END
```

**Semantic Router Fast Path:** Before reaching LangGraph, queries are checked against a FastEmbed-based router. Matches to `greeting` or `faq_admission` return instant canned responses with zero LLM latency.

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_health.py -v
```

## Error Handling

All errors follow a structured format:
```json
{
  "error": true,
  "error_code": "LLM_ERROR",
  "detail": "LLM service unavailable."
}
```

Custom exception classes in `app/core/errors.py`: `AppError`, `LLMError`, `RAGError`, `DatabaseError`, `ValidationError`, `StreamingError`.
