from sqlalchemy.orm import Session
from ..models.job import Job
from ..models.company import Company
from ..models.application import Application
from ..schemas.job import JobCreate, ApplicationCreate
from typing import List, Optional
from uuid import UUID
from sqlalchemy import or_, and_

def create_company(db: Session, owner_id: UUID, company_in: CompanyCreate):
    comp = Company(name=company_in.name, description=company_in.description, owner_id=owner_id)
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp

def get_company(db: Session, company_id: UUID):
    return db.query(Company).filter(Company.id == company_id).first()

def create_job(db: Session, job_in: JobCreate):
    job = Job(**job_in.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_job(db: Session, job_id: UUID):
    return db.query(Job).filter(Job.id == job_id).first()

def list_jobs(db: Session, q: Optional[str]=None, location: Optional[str]=None, job_type: Optional[str]=None, is_remote: Optional[bool]=None, limit: int=20, offset: int=0):
    query = db.query(Job)
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(Job.title.ilike(pattern), Job.description.ilike(pattern)))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter(Job.job_type == job_type)
    if is_remote is not None:
        query = query.filter(Job.is_remote == is_remote)
    total = query.count()
    items = query.order_by(Job.created_at.desc()).limit(limit).offset(offset).all()
    return items, total

def create_application(db: Session, job_id: UUID, user_id: UUID, app_in: ApplicationCreate):
    # prevent duplicate
    exists = db.query(Application).filter(Application.job_id == job_id, Application.user_id == user_id).first()
    if exists:
        return None
    app = Application(job_id=job_id, user_id=user_id, cover_letter=app_in.cover_letter, resume_id=app_in.resume_id)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

def list_applications_for_user(db: Session, user_id: UUID):
    return db.query(Application).filter(Application.user_id == user_id).all()

def list_applications_for_job(db: Session, job_id: UUID):
    return db.query(Application).filter(Application.job_id == job_id).all()
