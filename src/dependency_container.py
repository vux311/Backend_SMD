# Dependency Injection Container

from dependency_injector import containers, providers
from infrastructure.databases.mssql import session

from infrastructure.repositories.subject_repository import SubjectRepository
from services.subject_service import SubjectService

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for SMD services."""

    wiring_config = containers.WiringConfiguration(modules=[
        "src.api.controllers.subject_controller",
    ])

    # Provide a session object (singleton)
    db_session = providers.Object(session)

    # Repositories
    subject_repository = providers.Factory(
        SubjectRepository,
        session=db_session
    )

    # Services
    subject_service = providers.Factory(
        SubjectService,
        repository=subject_repository
    )