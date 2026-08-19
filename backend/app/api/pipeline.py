from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..api.deps import get_current_user
from ..schemas.pipeline import CandidateCreate, CandidateOut, StageChange, AssignPayload, NoteCreate, NoteOut, InterviewCreate, InterviewOut, OfferCreate, OfferOut
from ..db import crud_pipeline
from uuid import UUID
from typing import List

router = APIRouter(tags=["pipeline"])

@router.post("/pipelines/jobs/{job_id}/candidates", response_model=CandidateOut, status_code=status.HTTP_201_CREATED)
def create_candidate(job_id: UUID, payload: CandidateCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # ensure job_id matches payload
    if payload.job_id != job_id:
        raise HTTPException(status_code=400, detail="job_id mismatch")
    cand = crud_pipeline.create_candidate(db, payload, created_by=current_user.id)
    return cand

@router.get("/pipelines/jobs/{job_id}/candidates", response_model=List[CandidateOut])
def list_candidates(job_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    items = crud_pipeline.list_candidates_for_job(db, job_id)
    return items

@router.put("/pipelines/candidates/{candidate_id}/assign", response_model=CandidateOut)
def assign_candidate(candidate_id: UUID, payload: AssignPayload, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cand = crud_pipeline.get_candidate(db, candidate_id)
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
    cand.assigned_to = payload.user_id
    db.commit()
    db.refresh(cand)
    return cand

@router.post("/pipelines/candidates/{candidate_id}/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def add_note(candidate_id: UUID, payload: NoteCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cand = crud_pipeline.get_candidate(db, candidate_id)
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
    note = crud_pipeline.add_note(db, candidate_id, current_user.id, payload)
    return note

@router.post("/pipelines/candidates/{candidate_id}/interviews", response_model=InterviewOut, status_code=status.HTTP_201_CREATED)
def schedule_interview(candidate_id: UUID, payload: InterviewCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cand = crud_pipeline.get_candidate(db, candidate_id)
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
    interview = crud_pipeline.schedule_interview(db, candidate_id, payload)
    return interview

@router.post("/pipelines/candidates/{candidate_id}/offers", response_model=OfferOut, status_code=status.HTTP_201_CREATED)
def create_offer(candidate_id: UUID, payload: OfferCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cand = crud_pipeline.get_candidate(db, candidate_id)
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
    offer = crud_pipeline.create_offer(db, candidate_id, payload, job_id=cand.job_id)
    if offer is None:
        raise HTTPException(status_code=400, detail="Existing active offer exists")
    return offer

@router.put("/pipelines/offers/{offer_id}/status", response_model=OfferOut)
def update_offer(offer_id: UUID, status: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    offer = crud_pipeline.update_offer_status(db, offer_id, status)
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found or invalid")
    return offer
