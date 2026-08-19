import pytest
from httpx import AsyncClient
from backend.app.main import app
import os
from pathlib import Path

@pytest.mark.asyncio
async def test_profile_flow(tmp_path):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # register user
        payload = {"email": "student1@example.com", "password": "pass1234", "full_name": "Student One"}
        r = await ac.post("/api/v1/register", json=payload)
        assert r.status_code == 201
        # login
        r2 = await ac.post("/api/v1/login", json={"email": payload["email"], "password": payload["password"]})
        assert r2.status_code == 200
        token = r2.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # create/update profile
        profile_payload = {"bio": "CS student", "phone": "1234567890", "college": "ABC College", "graduation_year": 2025, "cgpa": 8.5}
        r3 = await ac.put("/api/v1/students/profile", json=profile_payload, headers=headers)
        assert r3.status_code == 200
        data = r3.json()
        assert data["college"] == "ABC College"
        # add education
        edu = {"degree": "B.Tech", "institution": "ABC College", "start_year": 2021, "end_year": 2025, "grade": "8.5"}
        r4 = await ac.post("/api/v1/students/education", json=edu, headers=headers)
        assert r4.status_code == 201
        # upload resume (simple bytes)
        files = {("file", ("resume.txt", b"My resume content example", "text/plain"))}
        # httpx AsyncClient expects files as list of tuples; use simple approach
        r5 = await ac.post("/api/v1/students/resume", headers=headers, files={"file": ("resume.txt", b"My resume content example", "text/plain")})
        assert r5.status_code == 201
        j = r5.json()
        assert "file_path" in j
        # cleanup file
        try:
            Path(j["file_path"]).unlink()
        except Exception:
            pass
