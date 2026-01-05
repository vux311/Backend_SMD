from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date, DateTime, Boolean,
    ForeignKey, Text, DECIMAL, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class NotificationTemplate(Base):
    __tablename__ = 'notification_templates'
    
    code = Column(String(50), primary_key=True)
    title_template = Column(String(255), nullable=False)
    body_template = Column(Text, nullable=False)
    channel = Column(String(20), default='SYSTEM')  # EMAIL, SMS, SYSTEM

