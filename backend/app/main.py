from fastapi import FastAPI
from .api import health
from .db import base  # ensure models imported for create_all
from .db.session import engine
from dotenv import load_dotenv
import os

load_dotenv()  # read .env in dev

# create DB tables if not exist (development convenience)
base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CareerHub AI - Backend", version="0.1")

app.include_router(health.router, prefix="/api/v1")
