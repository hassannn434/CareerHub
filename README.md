# CareerHub AI

CareerHub AI is a Smart Campus Career & Placement Platform. This repository contains the Phase 1 scaffold for CareerHub: a backend service, database schema, and a minimal ML-based job matcher designed to help students discover relevant opportunities.

Status: Phase 1 (scaffold)

Key components

- Backend: FastAPI-based scaffold exposing a versioned API (currently includes `/api/v1/health`).
- Database: PostgreSQL schema and local Docker Compose configuration (database/init.sql).
- ML: Minimal job matcher (ml/job_matcher.py) implementing TF-IDF + cosine similarity for basic resume-to-job matching.
- Infrastructure: Docker Compose configuration to run Postgres locally for development.

Goals for Phase 1

- Provide a clear project structure to build on.
- Include a working local development environment with Postgres and the FastAPI scaffold.
- Ship a simple, explainable ML prototype for job matching to iterate on.

Table of contents

- Features
- Tech stack
- Repository structure
- Getting started (local development)
- Database
- ML module
- Running the API
- Development
- Tests
- Contributing
- Roadmap
- License

Features

- Project folder scaffolded for backend, database, and ML experiments.
- Health-check endpoint for basic service liveness.
- TF-IDF + cosine similarity job matcher to prototype ranking and relevance.

Tech stack

- Python 3.10+ (or compatible)
- FastAPI
- Uvicorn
- PostgreSQL
- Docker & Docker Compose
- scikit-learn (for TF-IDF and cosine similarity in the ML prototype)

Repository structure

- backend/          - FastAPI app (entrypoint and routes)
- database/         - init.sql and DB-related helpers
- ml/               - job_matcher.py (TF-IDF + cosine similarity prototype)
- docker-compose.yml - Local Docker Compose to start Postgres
- README.md         - This file

Getting started (local development)

Prerequisites

- Docker and Docker Compose installed
- Python 3.10+ (for running the backend outside of Docker)

1) Start Postgres with Docker Compose

```bash
# from repository root
docker compose up -d
```

The Compose file starts a Postgres instance and mounts `database/init.sql` so the schema is ready for use.

2) Create and activate a virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.\.venv\Scripts\activate   # Windows PowerShell
pip install -r backend/requirements.txt
```

3) Configure environment variables

Create a `.env` file (or set environment variables) with the database connection string used by the backend. Example `.env`:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/careerhub
# Other env vars: SECRET_KEY, DEBUG, etc.
```

4) Run the FastAPI backend locally

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/api/v1/health to check the health endpoint. If you include FastAPI docs, the OpenAPI UI is typically at http://localhost:8000/docs

Database

- The SQL schema used in this project lives at `database/init.sql`.
- For migrations, Phase 2 suggests adding Alembic. For now the Docker Compose mounts `init.sql` to initialize the database.

ML module

- `ml/job_matcher.py` contains a minimal, explainable TF-IDF + cosine similarity implementation.
- Purpose: prototype ranking/resume-job matching behavior and provide a baseline to evaluate improvements (embeddings, fine-tuned models, etc.).
- How it works (high level):
  - Vectorize job descriptions and candidate profile text using TF-IDF.
  - Compute cosine similarity between candidate vector and job vectors.
  - Return sorted job scores.

Running and testing the ML prototype

You can run small experiments in a Python REPL or script. Example:

```python
from ml.job_matcher import JobMatcher

jobs = [
    {"id": 1, "title": "Backend Engineer", "description": "Python, REST, SQL"},
    {"id": 2, "title": "Data Scientist", "description": "Python, ML, statistics"},
]
matcher = JobMatcher(jobs)
scores = matcher.match("Experienced Python developer with SQL and REST API experience")
print(scores)
```

This prototype is intentionally simple — consider using transformer embeddings or fine-tuned models for production-grade matching.

API

- Current endpoints (Phase 1):
  - GET /api/v1/health — service health check

- Suggested Phase 2 endpoints:
  - Authentication endpoints (signup, login)
  - CRUD for jobs and profiles
  - Matching endpoint that accepts a profile/resume and returns ranked jobs

Development

- Add Pydantic schemas to validate requests/responses.
- Add Alembic for database migrations and a proper migration strategy.
- Expand test coverage and add CI (GitHub Actions) for linting and tests.

Tests

- Add unit tests for the ML module, database helpers, and API endpoints.
- Use pytest for running test suites.

Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository
2. Create a feature branch (git checkout -b feat/your-feature)
3. Make changes and add tests
4. Open a Pull Request with a clear description and testing notes

Roadmap (short)

- Phase 2: Authentication, Pydantic schemas, Alembic migrations, API for jobs/profiles, and frontend pages.
- Replace TF-IDF prototype with embeddings-based ranking (e.g., sentence-transformers) and evaluate.
- Add monitoring, CI, and containerized deployment docs.

License

This project is MIT-licensed. See LICENSE file for details (add one if missing).

Contact

Maintainer: hassannn434

Acknowledgements

This project scaffold was created to accelerate building a campus career & placement platform with an experimental ML matching component.
