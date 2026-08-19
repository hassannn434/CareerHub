import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..api.deps import get_current_active_user
from ..db import crud_profile
from ..schemas.profile import StudentProfileUpdate, StudentProfileOut, EducationCreate, ProjectCreate, CertificationCreate, InternshipCreate
from uuid import UUID
from pathlib import Path

router = APIRouter(tags=["students"])

@router.get("/students/profile", response_model=StudentProfileOut)
def read_profile(db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    # allow only students to use this endpoint
    from ..models.user import UserRole
    if getattr(current_user, "role", None) != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can access this endpoint")
    profile = crud_profile.get_profile_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile

@router.put("/students/profile", response_model=StudentProfileOut)
def update_profile(payload: StudentProfileUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    profile = crud_profile.create_or_update_profile(db, current_user.id, payload)
    return profile

@router.post("/students/education", status_code=status.HTTP_201_CREATED)
def add_education(payload: EducationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    try:
        edu = crud_profile.add_education(db, current_user.id, payload)
        return edu
    except ValueError:
        raise HTTPException(status_code=404, detail="Profile not found")

@router.post("/students/projects", status_code=status.HTTP_201_CREATED)
def add_project(payload: ProjectCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    try:
        proj = crud_profile.add_project(db, current_user.id, payload)
        return proj
    except ValueError:
        raise HTTPException(status_code=404, detail="Profile not found")

@router.post("/students/certifications", status_code=status.HTTP_201_CREATED)
def add_certification(payload: CertificationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    try:
        cert = crud_profile.add_certification(db, current_user.id, payload)
        return cert
    except ValueError:
        raise HTTPException(status_code=404, detail="Profile not found")

@router.post("/students/internships", status_code=status.HTTP_201_CREATED)
def add_internship(payload: InternshipCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    try:
        intern = crud_profile.add_internship(db, current_user.id, payload)
        return intern
    except ValueError:
        raise HTTPException(status_code=404, detail="Profile not found")

@router.post("/students/resume", status_code=status.HTTP_201_CREATED)
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    UPLOAD_ROOT = Path("uploads") / "resumes" / str(current_user.id)
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    filename = Path(file.filename).name
    dest = UPLOAD_ROOT / filename
    with dest.open("wb") as f:
        content = file.file.read()
        f.write(content)
    # Optionally extract text later
    resume = crud_profile.save_resume(db, current_user.id, str(dest))
    return {"id": str(resume.id), "file_path": resume.file_path}
