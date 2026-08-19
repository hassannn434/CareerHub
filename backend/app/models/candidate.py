from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid
from ..db.base import Base
from sqlalchemy.orm import relationship

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id", ondelete="SET NULL"), nullable=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    current_stage_id = Column(Integer, ForeignKey("pipeline_stages.id", ondelete="SET NULL"))
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status = Column(String, default="active")  # active, archived, hired, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    notes = relationship("CandidateNote", backref="candidate", cascade="all, delete-orphan")
    interviews = relationship("Interview", backref="candidate", cascade="all, delete-orphan")
    offers = relationship("Offer", backref="candidate", cascade="all, delete-orphan")
