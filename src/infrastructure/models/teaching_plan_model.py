from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class TeachingPlan(Base):
    __tablename__ = 'teaching_plans'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    syllabus_id = Column(BigInteger, ForeignKey('syllabuses.id', ondelete='CASCADE'), nullable=False)
    week = Column(Integer)
    topic = Column(Text)
    activity = Column(Text)
    assessment = Column(Text)
    
    # Relationships
    syllabus = relationship("Syllabus", back_populates="teaching_plans")