from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class Rubric(Base):
    __tablename__ = 'rubrics'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    component_id = Column(BigInteger, ForeignKey('assessment_components.id', ondelete='CASCADE'), nullable=False)
    criteria = Column(Text, nullable=False)
    max_score = Column(DECIMAL(3, 1), nullable=False)
    description_level_pass = Column(Text)
    description_level_fail = Column(Text)
    
    # Relationships
    component = relationship("AssessmentComponent", back_populates="rubrics")