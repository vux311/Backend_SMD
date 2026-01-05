from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class Program(Base):
    __tablename__ = 'programs'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    department_id = Column(BigInteger, ForeignKey('departments.id'), nullable=False)
    name = Column(String(255), nullable=False)
    total_credits = Column(Integer)
    
    # Relationships
    department = relationship("Department", back_populates="programs")
    outcomes = relationship("ProgramOutcome", back_populates="program")
    syllabuses = relationship("Syllabus", back_populates="program")





# from sqlalchemy import Column, Integer, String, DateTime
# from infrastructure.databases.base import Base

# class ProgramModel(Base):
#     __tablename__ = 'programs'
#     __table_args__ = {'extend_existing': True}  # Thêm dòng này

#     id = Column(Integer, primary_key=True)

#     title = Column(String(255), nullable=False)
#     description = Column(String(255), nullable=True)
#     status = Column(String(50), nullable=False)
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime) 
    
    
    # create table programs(
    #     id Int primary key,
    #     title nvarchar(255) not null,....
    # )