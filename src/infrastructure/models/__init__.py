from .user_model import User
from .user_role_model import UserRole
from .role_model import Role
from .faculty_model import Faculty
from .department_model import Department
from .program_model import Program
from .program_outcome_model import ProgramOutcome
from .subject_model import Subject
from .academic_year_model import AcademicYear
from .syllabus_model import Syllabus
from .syllabus_clo_model import SyllabusClo
from .syllabus_material_model import SyllabusMaterial
from .teaching_plan_model import TeachingPlan
from .assessment_scheme_model import AssessmentScheme
from .assessment_component_model import AssessmentComponent
from .rubric_model import Rubric
from .clo_plo_mapping_model import CloPloMapping

__all__ = [
    "User", "UserRole", "Role", "Faculty", "Department", "Program",
    "ProgramOutcome", "Subject", "AcademicYear", "Syllabus", "SyllabusClo",
    "SyllabusMaterial", "TeachingPlan", "AssessmentScheme", "AssessmentComponent", "Rubric",
    "CloPloMapping"
]
 