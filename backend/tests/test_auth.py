import pytest
from httpx import AsyncClient
from backend.app.main import app
import asyncio

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # register
        payload = {"email": "test1@example.com", "password": "strong-password", "full_name": "Test User"}
        r = await ac.post("/api/v1/register", json=payload)
        assert r.status_code == 201
        data = r.json()
        assert data["email"] == "test1@example.com"
        # login
        r2 = await ac.post("/api/v1/login", json=payload)
        assert r2.status_code == 200
        token_data = r2.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
