from sqlalchemy.orm import Session
from ..models.candidate import Candidate
from ..models.pipeline_stage import PipelineStage
from ..models.candidate_note import CandidateNote
from ..models.interview import Interview
from ..models.offer import Offer
from ..schemas.pipeline import CandidateCreate, NoteCreate, InterviewCreate, OfferCreate
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# Candidates
def create_candidate(db: Session, candidate_in: CandidateCreate, created_by: UUID = None):
    # if application_id provided, try to reuse existing candidate
    if candidate_in.application_id:
        existing = db.query(Candidate).filter(Candidate.application_id == candidate_in.application_id).first()
        if existing:
            return existing
    candidate = Candidate(application_id=candidate_in.application_id, job_id=candidate_in.job_id, assigned_to=candidate_in.assigned_to)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

def get_candidate(db: Session, candidate_id: UUID):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()

def list_candidates_for_job(db: Session, job_id: UUID, stage_id: Optional[int]=None):
    q = db.query(Candidate).filter(Candidate.job_id == job_id)
    if stage_id is not None:
        q = q.filter(Candidate.current_stage_id == stage_id)
    return q.all()

# Stages
def get_stage(db: Session, stage_id: int):
    return db.query(PipelineStage).filter(PipelineStage.id == stage_id).first()

# Notes
def add_note(db: Session, candidate_id: UUID, author_id: UUID, note_in: NoteCreate):
    note = CandidateNote(candidate_id=candidate_id, author_id=author_id, text=note_in.text)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

# Interviews
def schedule_interview(db: Session, candidate_id: UUID, interview_in: InterviewCreate):
    interview = Interview(candidate_id=candidate_id, scheduled_at=interview_in.scheduled_at, mode=interview_in.mode, participants=interview_in.participants)
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview

def add_interview_feedback(db: Session, interview_id: UUID, feedback: str, feedback_by: UUID):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        return None
    interview.feedback = feedback
    interview.feedback_by = feedback_by
    db.commit()
    db.refresh(interview)
    return interview

# Offers
def create_offer(db: Session, candidate_id: UUID, offer_in: OfferCreate, job_id: Optional[UUID] = None):
    # prevent duplicate active offers for same candidate
    existing = db.query(Offer).filter(Offer.candidate_id == candidate_id, Offer.status.in_(["draft","sent"])) .first()
    if existing:
        return None
    offer = Offer(candidate_id=candidate_id, job_id=job_id, salary=offer_in.salary, equity=offer_in.equity, terms=offer_in.terms)
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer

def update_offer_status(db: Session, offer_id: UUID, status: str):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        return None
    offer.status = status
    if status == "sent":
        offer.sent_at = datetime.utcnow()
    if status == "accepted":
        offer.accepted_at = datetime.utcnow()
    db.commit()
    db.refresh(offer)
    return offer
