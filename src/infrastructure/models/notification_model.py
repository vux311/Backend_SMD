from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text)
    link = Column(String(500))
    is_read = Column(Boolean, default=False)
    type = Column(String(50))  # SYSTEM, REVIEW, REMINDER
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")

