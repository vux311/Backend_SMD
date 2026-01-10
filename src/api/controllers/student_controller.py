from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.student_service import StudentService
from api.schemas.student_schema import StudentSubscriptionSchema, StudentReportSchema

student_bp = Blueprint('student', __name__, url_prefix='/student')
sub_schema = StudentSubscriptionSchema()
rep_schema = StudentReportSchema()

@student_bp.route('/subscribe', methods=['POST'])
@inject
def subscribe(service: StudentService = Provide[Container.student_service]):
    data = request.get_json() or {}
    # In production get user_id from token
    item = service.subscribe(data['student_id'], data['subject_id'])
    return jsonify(sub_schema.dump(item)), 201

@student_bp.route('/report', methods=['POST'])
@inject
def report(service: StudentService = Provide[Container.student_service]):
    data = request.get_json() or {}
    item = service.report_syllabus(data['student_id'], data['syllabus_id'], data['content'])
    return jsonify(rep_schema.dump(item)), 201

@student_bp.route('/reports', methods=['GET'])
@inject
def list_reports(service: StudentService = Provide[Container.student_service]):
    items = service.list_reports()
    return jsonify(rep_schema.dump(items, many=True)), 200