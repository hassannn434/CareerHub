from fastapi import FastAPI
from .api import health, auth, students, jobs
from .db import base  # ensure models imported for create_all
from .db.session import engine
from dotenv import load_dotenv

load_dotenv()  # read .env in dev

# create DB tables if not exist (development convenience)
base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CareerHub AI - Backend", version="0.4")

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(students.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
