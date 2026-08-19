from sqlalchemy import Column, Integer, SmallInteger, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class StudentSkill(Base):
    __tablename__ = "student_skills"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_profile_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    level = Column(SmallInteger, default=50)  # 0-100
    endorsements_count = Column(Integer, default=0)

    __table_args__ = (UniqueConstraint('student_profile_id', 'skill_id', name='uix_student_skill'),)
