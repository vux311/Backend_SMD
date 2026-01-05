from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base


class WorkflowLog(Base):
    __tablename__ = 'workflow_logs'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    syllabus_id = Column(BigInteger, ForeignKey('syllabuses.id'), nullable=False)
    actor_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    action = Column(String(50))  # SUBMIT, APPROVE, REJECT
    from_status = Column(String(50))
    to_status = Column(String(50))
    comment = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    syllabus = relationship("Syllabus", back_populates="workflow_logs")
    actor = relationship("User", back_populates="workflow_logs")
