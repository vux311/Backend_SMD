from typing import List
from infrastructure.repositories.assessment_clo_repository import AssessmentCloRepository

class AssessmentCloService:
    def __init__(self, repository: AssessmentCloRepository, component_repository=None, syllabus_clo_repository=None):
        self.repository = repository
        self.component_repository = component_repository
        self.syllabus_clo_repository = syllabus_clo_repository

    def get_clos_for_component(self, component_id: int) -> List:
        return self.repository.get_clos_by_component(component_id)

    def add_mapping(self, component_id: int, syllabus_clo_id: int):
        if not self.component_repository.get_by_id(component_id):
            raise ValueError('Invalid component_id')
        if not self.syllabus_clo_repository.get_by_id(syllabus_clo_id):
            raise ValueError('Invalid syllabus_clo_id')
        return self.repository.add_mapping(component_id, syllabus_clo_id)

    def remove_mapping(self, component_id: int, syllabus_clo_id: int) -> bool:
        return self.repository.remove_mapping(component_id, syllabus_clo_id)