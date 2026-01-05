# Thêm BigInteger vào dòng import
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger
from infrastructure.databases.base import Base

class CourseRegisterModel(Base):
    __tablename__ = 'course_register'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    
    # SỬA: Dùng BigInteger để khớp với users.id
    user_id = Column(BigInteger, ForeignKey('users.id')) 
    
    # Giữ nguyên Integer cho course_id vì bảng courses dùng Integer (trừ khi bạn đã sửa bảng courses thành BigInteger)
    course_id = Column(Integer, ForeignKey('courses.id'))