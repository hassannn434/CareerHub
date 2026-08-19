from sqlalchemy import Column, DateTime, String, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, func
import uuid
from ..db.base import Base

class Offer(Base):
    __tablename__ = "offers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    salary = Column(Numeric)
    equity = Column(String)
    terms = Column(Text)
    status = Column(String, default="draft")  # draft, sent, accepted, declined
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True))
    accepted_at = Column(DateTime(timezone=True))
