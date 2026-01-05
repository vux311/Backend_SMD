from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class SystemSetting(Base):
    __tablename__ = 'system_settings'
    
    key = Column(String(50), primary_key=True)
    value = Column(Text, nullable=False)
    type = Column(String(20), default='STRING')
    description = Column(String(255), nullable=True)