from sqlalchemy import Column, String, Text, Date, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..db.base import Base
from sqlalchemy import func, DateTime

class Job(Base):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    location = Column(String)
    work_mode = Column(String)
    experience_min = Column(Integer)
    experience_max = Column(Integer)
    eligibility = Column(Text)
    salary = Column(String)
    stipend = Column(String)
    application_deadline = Column(Date)
    description = Column(Text)
    posted_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(Date)
    is_published = Column(Boolean, default=True)
