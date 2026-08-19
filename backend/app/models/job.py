from sqlalchemy import Column, String, DateTime, Boolean, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, func
import uuid
from ..db.base import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    is_remote = Column(Boolean, default=False)
    job_type = Column(String)  # e.g., full_time, part_time, contract
    salary_min = Column(Numeric)
    salary_max = Column(Numeric)
    skills = Column(String)  # comma-separated skill ids or names
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
