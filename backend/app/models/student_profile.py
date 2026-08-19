from sqlalchemy import Column, String, DateTime, Numeric, Integer, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..db.base import Base
from sqlalchemy.orm import relationship

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    bio = Column(String)
    phone = Column(String)
    college = Column(String)
    graduation_year = Column(Integer)
    cgpa = Column(Numeric(3,2))
    linked_in = Column(String)
    github = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    user = relationship("User", backref="student_profile", uselist=False)
    skills = relationship("StudentSkill", backref="student_profile", cascade="all, delete-orphan")
    educations = relationship("Education", backref="student_profile", cascade="all, delete-orphan")
    projects = relationship("Project", backref="student_profile", cascade="all, delete-orphan")
    certifications = relationship("Certification", backref="student_profile", cascade="all, delete-orphan")
    internships = relationship("Internship", backref="student_profile", cascade="all, delete-orphan")
    resumes = relationship("Resume", backref="student_profile", cascade="all, delete-orphan")
