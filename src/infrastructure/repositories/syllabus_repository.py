from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.mssql import session
from infrastructure.models.syllabus_model import Syllabus

class SyllabusRepository:
    def __init__(self, session: Session = session):
        self.session = session

    def get_all(self) -> List[Syllabus]:
        return self.session.query(Syllabus).all()

    def get_by_id(self, id: int) -> Optional[Syllabus]:
        return self.session.query(Syllabus).filter_by(id=id).first()

    def get_by_subject_id(self, subject_id: int) -> List[Syllabus]:
        return self.session.query(Syllabus).filter_by(subject_id=subject_id).all()

    def create(self, data: dict) -> Syllabus:
        s = Syllabus(**data)
        self.session.add(s)
        self.session.commit()
        self.session.refresh(s)
        return s

    def update(self, id: int, data: dict) -> Optional[Syllabus]:
        s = self.get_by_id(id)
        if not s:
            return None
        for key, value in data.items():
            if hasattr(s, key):
                setattr(s, key, value)
        self.session.commit()
        self.session.refresh(s)
        return s

    def delete(self, id: int) -> bool:
        s = self.get_by_id(id)
        if not s:
            return False
        self.session.delete(s)
        self.session.commit()
        return True