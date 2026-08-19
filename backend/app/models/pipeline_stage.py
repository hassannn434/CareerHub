from sqlalchemy import Column, Integer, String, Boolean
from ..db.base import Base

class PipelineStage(Base):
    __tablename__ = "pipeline_stages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    order = Column(Integer, nullable=False)
    is_final = Column(Boolean, default=False)
