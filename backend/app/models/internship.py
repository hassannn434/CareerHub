from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class Internship(Base):
    __tablename__ = "internships"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_profile_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    company = Column(String, nullable=False)
    role = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
