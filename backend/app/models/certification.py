from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class Certification(Base):
    __tablename__ = "certifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_profile_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    authority = Column(String)
    year = Column(Integer)
    url = Column(String)
