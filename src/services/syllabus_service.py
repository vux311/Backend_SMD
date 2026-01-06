from typing import List, Optional
from infrastructure.repositories.syllabus_repository import SyllabusRepository

class SyllabusService:
    def __init__(self, repository: SyllabusRepository,
                 subject_repository=None,
                 program_repository=None,
                 academic_year_repository=None,
                 user_repository=None):
        self.repository = repository
        self.subject_repository = subject_repository
        self.program_repository = program_repository
        self.academic_year_repository = academic_year_repository
        self.user_repository = user_repository

    def list_syllabuses(self) -> List:
        return self.repository.get_all()

    def get_syllabus(self, id: int):
        return self.repository.get_by_id(id)

    def get_by_subject(self, subject_id: int):
        return self.repository.get_by_subject_id(subject_id)

    def create_syllabus(self, data: dict):
        # Validate foreign keys
        subject_id = data.get('subject_id')
        program_id = data.get('program_id')
        academic_year_id = data.get('academic_year_id')
        lecturer_id = data.get('lecturer_id')

        if not subject_id or not self.subject_repository.get_by_id(subject_id):
            raise ValueError('Invalid subject_id')
        if not program_id or not self.program_repository.get_by_id(program_id):
            raise ValueError('Invalid program_id')
        if not academic_year_id or not self.academic_year_repository.get_by_id(academic_year_id):
            raise ValueError('Invalid academic_year_id')
        if not lecturer_id or not self.user_repository.get_by_id(lecturer_id):
            raise ValueError('Invalid lecturer_id')

        # Defaults
        data.setdefault('status', 'DRAFT')

        return self.repository.create(data)

    def update_syllabus(self, id: int, data: dict):
        return self.repository.update(id, data)

    def delete_syllabus(self, id: int) -> bool:
        return self.repository.delete(id)