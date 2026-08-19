from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_profile_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    degree = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    start_year = Column(Integer)
    end_year = Column(Integer)
    grade = Column(String)
    description = Column(Text)
