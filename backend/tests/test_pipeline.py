import pytest
from httpx import AsyncClient
from backend.app.main import app
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_pipeline_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # setup company, job, application -> candidate
        comp_user = {"email": "comp2@example.com", "password": "pass1234", "full_name": "Company Owner 2"}
        r = await ac.post("/api/v1/register", json=comp_user)
        assert r.status_code == 201
        r2 = await ac.post("/api/v1/login", json={"email": comp_user["email"], "password": comp_user["password"]})
        token_comp = r2.json()["access_token"]
        headers_comp = {"Authorization": f"Bearer {token_comp}"}
        # create company
        r3 = await ac.post("/api/v1/companies", json={"name": "Beta Corp" , "description": "Hiring"}, headers=headers_comp)
        assert r3.status_code == 201
        company = r3.json()
        # create job
        job_payload = {"company_id": company["id"], "title": "QA Engineer", "description": "Test things", "location": "Onsite", "is_remote": False}
        r4 = await ac.post("/api/v1/jobs", json=job_payload, headers=headers_comp)
        assert r4.status_code == 201
        job = r4.json()
        # create student and application -> candidate
        student = {"email": "stud2@example.com", "password": "pass1234", "full_name": "Student 2"}
        await ac.post("/api/v1/register", json=student)
        r5 = await ac.post("/api/v1/login", json={"email": student["email"], "password": student["password"]})
        token_stud = r5.json()["access_token"]
        headers_stud = {"Authorization": f"Bearer {token_stud}"}
        # apply
        app_payload = {"cover_letter": "Please hire me"}
        r6 = await ac.post(f"/api/v1/jobs/{job['id']}/apply", json=app_payload, headers=headers_stud)
        assert r6.status_code == 201
        application = r6.json()
        # create candidate from application: we will hit pipeline create endpoint
        cand_payload = {"application_id": application["id"], "job_id": job["id"]}
        r7 = await ac.post(f"/api/v1/pipelines/jobs/{job['id']}/candidates", json=cand_payload, headers=headers_comp)
        assert r7.status_code == 201
        candidate = r7.json()
        # add note
        note_payload = {"text": "Initial screening passed"}
        r8 = await ac.post(f"/api/v1/pipelines/candidates/{candidate['id']}/notes", json=note_payload, headers=headers_comp)
        assert r8.status_code == 201
        # schedule interview
        sched = (datetime.utcnow() + timedelta(days=2)).isoformat()
        interview_payload = {"scheduled_at": sched, "mode": "video", "participants": ["comp2@example.com"]}
        r9 = await ac.post(f"/api/v1/pipelines/candidates/{candidate['id']}/interviews", json=interview_payload, headers=headers_comp)
        assert r9.status_code == 201
        interview = r9.json()
        # create offer
        offer_payload = {"salary": 60000, "equity": "0.1%", "terms": "Standard"}
        r10 = await ac.post(f"/api/v1/pipelines/candidates/{candidate['id']}/offers", json=offer_payload, headers=headers_comp)
        assert r10.status_code == 201
        offer = r10.json()
        # send offer
        r11 = await ac.put(f"/api/v1/pipelines/offers/{offer['id']}/status", params={"status": "sent"}, headers=headers_comp)
        assert r11.status_code == 200
        # accept offer
        r12 = await ac.put(f"/api/v1/pipelines/offers/{offer['id']}/status", params={"status": "accepted"}, headers=headers_comp)
        assert r12.status_code == 200
