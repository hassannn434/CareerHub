from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CandidateCreate(BaseModel):
    application_id: Optional[UUID]
    job_id: UUID
    assigned_to: Optional[UUID]

class CandidateOut(BaseModel):
    id: UUID
    application_id: Optional[UUID]
    job_id: UUID
    current_stage_id: Optional[int]
    assigned_to: Optional[UUID]
    status: str

    class Config:
        orm_mode = True

class StageChange(BaseModel):
    target_stage_id: int
    comment: Optional[str]

class AssignPayload(BaseModel):
    user_id: UUID

class NoteCreate(BaseModel):
    text: str

class NoteOut(BaseModel):
    id: UUID
    candidate_id: UUID
    author_id: Optional[UUID]
    text: str

    class Config:
        orm_mode = True

class InterviewCreate(BaseModel):
    scheduled_at: datetime
    mode: Optional[str]
    participants: Optional[List[str]]

class InterviewOut(BaseModel):
    id: UUID
    candidate_id: UUID
    scheduled_at: datetime
    mode: Optional[str]
    participants: Optional[List[str]]
    feedback: Optional[str]

    class Config:
        orm_mode = True

class OfferCreate(BaseModel):
    salary: Optional[float]
    equity: Optional[str]
    terms: Optional[str]

class OfferOut(BaseModel):
    id: UUID
    candidate_id: UUID
    job_id: Optional[UUID]
    salary: Optional[float]
    equity: Optional[str]
    terms: Optional[str]
    status: str

    class Config:
        orm_mode = True
