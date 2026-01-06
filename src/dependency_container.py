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
from infrastructure.repositories.academic_year_repository import AcademicYearRepository
from services.academic_year_service import AcademicYearService
from infrastructure.repositories.program_repository import ProgramRepository
from services.program_service import ProgramService
from infrastructure.repositories.syllabus_repository import SyllabusRepository
from services.syllabus_service import SyllabusService
from infrastructure.repositories.syllabus_clo_repository import SyllabusCloRepository
from services.syllabus_clo_service import SyllabusCloService
from infrastructure.repositories.syllabus_material_repository import SyllabusMaterialRepository
from services.syllabus_material_service import SyllabusMaterialService
from infrastructure.repositories.teaching_plan_repository import TeachingPlanRepository
from services.teaching_plan_service import TeachingPlanService

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for SMD services."""

    wiring_config = containers.WiringConfiguration(modules=[
        "api.controllers.subject_controller",
        "api.controllers.faculty_controller",
        "api.controllers.department_controller",
        "api.controllers.role_controller",
        "api.controllers.user_controller",
        "api.controllers.academic_year_controller",
        "api.controllers.program_controller",
        "api.controllers.syllabus_controller",
        "api.controllers.syllabus_clo_controller",
        "api.controllers.syllabus_material_controller",
        "api.controllers.teaching_plan_controller",
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

    academic_year_repository = providers.Factory(
        AcademicYearRepository,
        session=db_session
    )

    program_repository = providers.Factory(
        ProgramRepository,
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

    academic_year_service = providers.Factory(
        AcademicYearService,
        repository=academic_year_repository
    )

    program_service = providers.Factory(
        ProgramService,
        repository=program_repository
    )

    syllabus_repository = providers.Factory(
        SyllabusRepository,
        session=db_session
    )

    syllabus_clo_repository = providers.Factory(
        SyllabusCloRepository,
        session=db_session
    )

    syllabus_material_repository = providers.Factory(
        SyllabusMaterialRepository,
        session=db_session
    )

    teaching_plan_repository = providers.Factory(
        TeachingPlanRepository,
        session=db_session
    )

    academic_year_service = providers.Factory(
        AcademicYearService,
        repository=academic_year_repository
    )

    program_service = providers.Factory(
        ProgramService,
        repository=program_repository
    )

    syllabus_service = providers.Factory(
        SyllabusService,
        repository=syllabus_repository,
        subject_repository=subject_repository,
        program_repository=program_repository,
        academic_year_repository=academic_year_repository,
        user_repository=user_repository
    )

    syllabus_clo_service = providers.Factory(
        SyllabusCloService,
        repository=syllabus_clo_repository,
        syllabus_repository=syllabus_repository
    )

    syllabus_material_service = providers.Factory(
        SyllabusMaterialService,
        repository=syllabus_material_repository,
        syllabus_repository=syllabus_repository
    )

    teaching_plan_service = providers.Factory(
        TeachingPlanService,
        repository=teaching_plan_repository,
        syllabus_repository=syllabus_repository
    )

    role_service = providers.Factory(
        RoleService,
        repository=role_repository
    )

    user_service = providers.Factory(
        UserService,
        repository=user_repository
    )