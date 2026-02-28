# Systex Mini Hybrid-RAG Demo (FastAPI + Next.js)

A minimal, runnable project that demonstrates an enterprise-style assistant pipeline:
SSO/Tenant/RBAC -> Hybrid Retrieval (Vector + SQL + Graph) -> Context Builder -> LLM Gateway -> Answer w/ Citations -> Observability & Governance.

## Tech Stack
### Backend
- Python 3.11
- FastAPI (API/BFF, SSE streaming)
- JWT (Mock SSO)
- Tenant isolation (tenant claim)
- RBAC (role-based access control)
- SQLite + SQLAlchemy (structured retrieval / ERP-CRM simulation)
- TF-IDF (vector-like retrieval simulation, no external embeddings required)
- Simple graph expansion (entity -> neighbors)
- Audit logging (latency, retrieval hits, token cost estimate)
- Basic governance: prompt injection detection + output sanitization (demo-level)

### Frontend
- Next.js 14 + React 18
- Simple chat UI
- SSE streaming consumption

## How to Run (Docker)
```bash
docker compose up --build