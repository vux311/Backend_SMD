from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class SystemAuditLog(Base):
    __tablename__ = 'system_audit_logs'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    action_type = Column(String(50), nullable=False)
    resource_target = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    details = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User")

