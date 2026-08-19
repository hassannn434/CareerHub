# Architecture

This document describes the high-level architecture for CareerHub AI Phase 1.

Components:

- Frontend: React SPA (frontend/) — communicates with backend via REST APIs.
- Backend: FastAPI app (backend/app/) — provides API endpoints, JWT auth (Phase 2), and AI endpoints.
- Database: PostgreSQL (database/) — normalized schema in init.sql; use Alembic for migrations in Phase 2.
- ML: Standalone Python module (ml/) using scikit-learn TF-IDF + cosine similarity for explainable job matching.

Data flow:

1. Frontend calls backend REST APIs.
2. Backend reads/writes to Postgres.
3. Backend uses ML module to compute job-match scores and career readiness.

Security & DevOps:

- Use environment variables for secrets (.env)
- Use docker-compose for local Postgres
- Use CI to run tests and linters (to be added)
