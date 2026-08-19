from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CompanyCreate(BaseModel):
    name: str
    description: Optional[str]

class CompanyOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    owner_id: Optional[UUID]

    class Config:
        orm_mode = True

class JobCreate(BaseModel):
    company_id: UUID
    title: str
    description: Optional[str]
    location: Optional[str]
    is_remote: Optional[bool] = False
    job_type: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    skills: Optional[str]
    expires_at: Optional[datetime]

class JobOut(BaseModel):
    id: UUID
    company_id: UUID
    title: str
    description: Optional[str]
    location: Optional[str]
    is_remote: Optional[bool]
    job_type: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    skills: Optional[str]
    created_at: Optional[datetime]
    expires_at: Optional[datetime]

    class Config:
        orm_mode = True

class ApplicationCreate(BaseModel):
    cover_letter: Optional[str]
    resume_id: Optional[UUID]

class ApplicationOut(BaseModel):
    id: UUID
    job_id: UUID
    user_id: UUID
    status: str
    cover_letter: Optional[str]
    resume_id: Optional[UUID]
    applied_at: Optional[datetime]

    class Config:
        orm_mode = True
