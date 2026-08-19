# Alembic helper README

This folder contains a template env.py for Alembic. To initialize migrations locally:

1. cd backend
2. pip install alembic
3. alembic init alembic
4. Replace alembic/env.py with backend/alembic/env.py from this repo or merge accordingly.
5. Configure alembic.ini sqlalchemy.url or set DATABASE_URL in your environment.
6. Run: alembic revision --autogenerate -m "Initial"
7. Run: alembic upgrade head
