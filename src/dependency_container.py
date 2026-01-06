# Dependency Injection Container

from dependency_injector import containers, providers
from infrastructure.databases.mssql import session

from infrastructure.repositories.subject_repository import SubjectRepository
from services.subject_service import SubjectService
from infrastructure.repositories.faculty_repository import FacultyRepository
from services.faculty_service import FacultyService
from infrastructure.repositories.department_repository import DepartmentRepository
from services.department_service import DepartmentService

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for SMD services."""

    wiring_config = containers.WiringConfiguration(modules=[
        "api.controllers.subject_controller",
        "api.controllers.faculty_controller",
        "api.controllers.department_controller",
    ])

    # Provide a session object (singleton)
    db_session = providers.Object(session)

    # Repositories
    subject_repository = providers.Factory(
        SubjectRepository,
        session=db_session
    )

    faculty_repository = providers.Factory(
        FacultyRepository,
        session=db_session
    )

    department_repository = providers.Factory(
        DepartmentRepository,
        session=db_session
    )

    # Services
    subject_service = providers.Factory(
        SubjectService,
        repository=subject_repository
    )

    faculty_service = providers.Factory(
        FacultyService,
        repository=faculty_repository
    )

    department_service = providers.Factory(
        DepartmentService,
        repository=department_repository
    )