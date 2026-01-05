# Thêm BigInteger vào dòng import
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger
from infrastructure.databases.base import Base

class AppointmentModel(Base):
    __tablename__ = 'appointments'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'))
    
    # SỬA: Dùng BigInteger
    user_id = Column(BigInteger,  ForeignKey('users.id'))
    
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    url_online = Column(String(255), nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)