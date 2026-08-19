from sqlalchemy import Column, String, DateTime, Boolean, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, func
import uuid
from ..db.base import Base
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "companies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    jobs = relationship("Job", backref="company", cascade="all, delete-orphan")
