from pydantic import BaseModel, HttpUrl
from typing import Optional
from uuid import UUID
from datetime import date

class EducationCreate(BaseModel):
    degree: str
    institution: str
    start_year: Optional[int]
    end_year: Optional[int]
    grade: Optional[str]
    description: Optional[str]

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str]
    repo_url: Optional[HttpUrl]
    tech_stack: Optional[str]

class CertificationCreate(BaseModel):
    name: str
    authority: Optional[str]
    year: Optional[int]
    url: Optional[HttpUrl]

class InternshipCreate(BaseModel):
    company: str
    role: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    description: Optional[str]

class StudentProfileUpdate(BaseModel):
    bio: Optional[str]
    phone: Optional[str]
    college: Optional[str]
    graduation_year: Optional[int]
    cgpa: Optional[float]
    linked_in: Optional[HttpUrl]
    github: Optional[HttpUrl]

class StudentProfileOut(BaseModel):
    id: UUID
    user_id: UUID
    bio: Optional[str]
    phone: Optional[str]
    college: Optional[str]
    graduation_year: Optional[int]
    cgpa: Optional[float]
    linked_in: Optional[HttpUrl]
    github: Optional[HttpUrl]

    class Config:
        orm_mode = True
