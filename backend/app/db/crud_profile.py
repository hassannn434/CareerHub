from sqlalchemy.orm import Session
from ..models.student_profile import StudentProfile
from ..models.education import Education
from ..models.project import Project
from ..models.certification import Certification
from ..models.internship import Internship
from ..models.resume import Resume
from ..schemas.profile import StudentProfileUpdate, EducationCreate, ProjectCreate, CertificationCreate, InternshipCreate
from uuid import UUID

def get_profile_by_user_id(db: Session, user_id: UUID):
    return db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()

def create_or_update_profile(db: Session, user_id: UUID, update_in: StudentProfileUpdate):
    profile = get_profile_by_user_id(db, user_id)
    data = update_in.dict(exclude_none=True)
    if not profile:
        profile = StudentProfile(user_id=user_id, **data)
        db.add(profile)
    else:
        for k, v in data.items():
            setattr(profile, k, v)
    db.commit()
    db.refresh(profile)
    return profile

def add_education(db: Session, user_id: UUID, edu_in: EducationCreate):
    profile = get_profile_by_user_id(db, user_id)
    if not profile:
        raise ValueError("Profile not found")
    edu = Education(student_profile_id=profile.id, **edu_in.dict())
    db.add(edu)
    db.commit()
    db.refresh(edu)
    return edu

def add_project(db: Session, user_id: UUID, proj_in: ProjectCreate):
    profile = get_profile_by_user_id(db, user_id)
    if not profile:
        raise ValueError("Profile not found")
    proj = Project(student_profile_id=profile.id, **proj_in.dict())
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

def add_certification(db: Session, user_id: UUID, cert_in: CertificationCreate):
    profile = get_profile_by_user_id(db, user_id)
    if not profile:
        raise ValueError("Profile not found")
    cert = Certification(student_profile_id=profile.id, **cert_in.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

def add_internship(db: Session, user_id: UUID, intern_in: InternshipCreate):
    profile = get_profile_by_user_id(db, user_id)
    if not profile:
        raise ValueError("Profile not found")
    intern = Internship(student_profile_id=profile.id, **intern_in.dict())
    db.add(intern)
    db.commit()
    db.refresh(intern)
    return intern

def save_resume(db: Session, user_id: UUID, file_path: str, text_extracted: str = None):
    resume = Resume(user_id=user_id, file_path=file_path, text_extracted=text_extracted)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume
