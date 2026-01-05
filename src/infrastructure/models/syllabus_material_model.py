from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class SyllabusMaterial(Base):
    __tablename__ = 'syllabus_materials'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    syllabus_id = Column(BigInteger, ForeignKey('syllabuses.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50), nullable=False)  # MAIN, REFERENCE
    title = Column(String(555), nullable=False)
    author = Column(String(255))
    publisher = Column(String(255))
    published_year = Column(Integer)
    isbn = Column(String(50))
    url = Column(Text, nullable=True)
    
    # Relationships
    syllabus = relationship("Syllabus", back_populates="materials")
