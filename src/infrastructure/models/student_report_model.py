from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class StudentReport(Base):
    __tablename__ = 'student_reports'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    syllabus_id = Column(BigInteger, ForeignKey('syllabuses.id'), nullable=False)
    student_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(20), default='PENDING')  # PENDING, RESOLVED, REJECTED
    admin_note = Column(Text)
    
    # Relationships
    syllabus = relationship("Syllabus", back_populates="student_reports")
    student = relationship("User")