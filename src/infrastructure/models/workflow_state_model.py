from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class WorkflowState(Base):
    __tablename__ = 'workflow_states'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    color = Column(String(20))
    is_final = Column(Boolean, default=False)
    
    # Relationships
    transitions_from = relationship("WorkflowTransition", 
                                   foreign_keys="WorkflowTransition.from_state_id",
                                   back_populates="from_state")
    transitions_to = relationship("WorkflowTransition",
                                 foreign_keys="WorkflowTransition.to_state_id",
                                 back_populates="to_state")
    current_workflows = relationship("SyllabusCurrentWorkflow", back_populates="current_state")
