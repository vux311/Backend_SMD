from infrastructure.databases.mssql import init_mssql
from infrastructure.models import (
    course_register_model, 
    todo_model, 
    user_model, 
    course_model, 
    consultant_model, 
    appointment_model, 
    program_model, 
    feedback_model,
    survey_model,
    academic_year_model,
    ai_auditlog_model,
    appointment_model,
    assessment_clo_model,
    assessment_component_model,
    assessment_scheme_model,
    clo_plo_mapping_model,
    consultant_model,
    course_model,
    course_register_model,
    department_model,
    faculty_model,
    feedback_model,
    file_model,
    notification_model,
    notification_template_model,
    program_model,
    program_outcome_model,
    role_model,
    rubric_model,
    student_report_model,
    student_subscription_model,
    subject_model,
    subject_relationship_model,
    survey_model,
    syllabus_clo_model,
    syllabus_comment_model,
    syllabus_current_workflow,
    syllabus_material_model,
    syllabus_model,
    system_auditlog_model,
    system_setting_model,
    teaching_plan_model,
    todo_model,
    user_model,
    user_role_model,
    workflow_log_model,
    workflow_state_model,
    workflow_transition_model
    

)
from infrastructure.models.auth import auth_user_model, auth_role_model,auth_funtion_model
from infrastructure.models.sell import sell_customer_model, sell_product_model, sell_invoice_model
from infrastructure.models.pay import pay_tran_model

def init_db(app):
    init_mssql(app)
    
# Migration Entities -> tables
from infrastructure.databases.mssql import Base