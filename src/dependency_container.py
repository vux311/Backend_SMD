# Dependency Injection Container

from dependency_injector import containers, providers
from infrastructure.databases.mssql import session

from infrastructure.repositories.subject_repository import SubjectRepository
from services.subject_service import SubjectService
from infrastructure.repositories.faculty_repository import FacultyRepository
from services.faculty_service import FacultyService
from infrastructure.repositories.department_repository import DepartmentRepository
from services.department_service import DepartmentService
from infrastructure.repositories.role_repository import RoleRepository
from services.role_service import RoleService
from infrastructure.repositories.user_repository import UserRepository
from services.user_service import UserService

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for SMD services."""

    wiring_config = containers.WiringConfiguration(modules=[
        "api.controllers.subject_controller",
        "api.controllers.faculty_controller",
        "api.controllers.department_controller",
        "api.controllers.role_controller",
        "api.controllers.user_controller",
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

    role_repository = providers.Factory(
        RoleRepository,
        session=db_session
    )

    user_repository = providers.Factory(
        UserRepository,
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

    role_service = providers.Factory(
        RoleService,
        repository=role_repository
    )

    user_service = providers.Factory(
        UserService,
        repository=user_repository
    )