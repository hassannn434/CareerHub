from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..api.deps import get_current_user
from ..schemas.job import CompanyCreate, CompanyOut, JobCreate, JobOut, ApplicationCreate, ApplicationOut
from ..db import crud_job
from uuid import UUID
from typing import List, Optional

router = APIRouter(tags=["jobs"])

@router.post("/companies", response_model=CompanyOut, status_code=status.HTTP_201_CREATED)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    comp = crud_job.create_company(db, current_user.id, payload)
    return comp

@router.post("/jobs", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # only company owner or admin can create job for company
    comp = crud_job.get_company(db, payload.company_id)
    from ..models.user import UserRole
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")
    if comp.owner_id != current_user.id and getattr(current_user, 'role', None) != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create job for this company")
    job = crud_job.create_job(db, payload)
    return job

@router.get("/jobs", response_model=List[JobOut])
def list_jobs(q: Optional[str] = None, location: Optional[str] = None, job_type: Optional[str] = None, is_remote: Optional[bool] = None, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    items, total = crud_job.list_jobs(db, q=q, location=location, job_type=job_type, is_remote=is_remote, limit=limit, offset=offset)
    return items

@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/jobs/{job_id}/apply", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def apply_job(job_id: UUID, payload: ApplicationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # only students (or any authenticated user) can apply — enforce student role if desired
    from ..models.user import UserRole
    if getattr(current_user, 'role', None) != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can apply")
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    app = crud_job.create_application(db, job_id, current_user.id, payload)
    if app is None:
        raise HTTPException(status_code=400, detail="Already applied")
    return app

@router.get("/users/me/applications", response_model=List[ApplicationOut])
def my_applications(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    apps = crud_job.list_applications_for_user(db, current_user.id)
    return apps

@router.get("/jobs/{job_id}/applications", response_model=List[ApplicationOut])
def job_applications(job_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    # only company owner or admin
    from ..models.user import UserRole
    comp = crud_job.get_company(db, job.company_id)
    if comp is None:
        raise HTTPException(status_code=404, detail="Company not found")
    if comp.owner_id != current_user.id and getattr(current_user, 'role', None) != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    apps = crud_job.list_applications_for_job(db, job_id)
    return apps
