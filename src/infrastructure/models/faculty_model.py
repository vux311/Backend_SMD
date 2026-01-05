from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.databases.base import Base


class Faculty(Base):
    __tablename__ = 'faculties'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    
    # Relationships
    departments = relationship("Department", back_populates="faculty")