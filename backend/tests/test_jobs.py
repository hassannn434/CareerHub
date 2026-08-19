import pytest
from httpx import AsyncClient
from backend.app.main import app

@pytest.mark.asyncio
async def test_job_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create company user
        comp_user = {"email": "comp@example.com", "password": "pass1234", "full_name": "Company Owner"}
        r = await ac.post("/api/v1/register", json=comp_user)
        assert r.status_code == 201
        # login company user
        r2 = await ac.post("/api/v1/login", json={"email": comp_user["email"], "password": comp_user["password"]})
        token_comp = r2.json()["access_token"]
        headers_comp = {"Authorization": f"Bearer {token_comp}"}
        # create company
        r3 = await ac.post("/api/v1/companies", json={"name": "Acme Corp", "description": "We hire"}, headers=headers_comp)
        assert r3.status_code == 201
        company = r3.json()
        # create job
        job_payload = {"company_id": company["id"], "title": "Software Engineer", "description": "Build things", "location": "Remote", "is_remote": True, "job_type": "full_time"}
        r4 = await ac.post("/api/v1/jobs", json=job_payload, headers=headers_comp)
        assert r4.status_code == 201
        job = r4.json()
        # create student and apply
        student = {"email": "stud@example.com", "password": "pass1234", "full_name": "Student"}
        await ac.post("/api/v1/register", json=student)
        r5 = await ac.post("/api/v1/login", json={"email": student["email"], "password": student["password"]})
        token_stud = r5.json()["access_token"]
        headers_stud = {"Authorization": f"Bearer {token_stud}"}
        # apply
        app_payload = {"cover_letter": "I want this job"}
        r6 = await ac.post(f"/api/v1/jobs/{job['id']}/apply", json=app_payload, headers=headers_stud)
        assert r6.status_code == 201
        # applying again should fail
        r7 = await ac.post(f"/api/v1/jobs/{job['id']}/apply", json=app_payload, headers=headers_stud)
        assert r7.status_code == 400
