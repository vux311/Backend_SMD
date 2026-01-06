from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.assessment_clo_service import AssessmentCloService
from api.schemas.assessment_clo_mapping_schema import AssessmentCloMappingSchema

assessment_clo_bp = Blueprint('assessment_clo_map', __name__, url_prefix='/assessment-clos')

schema = AssessmentCloMappingSchema()

@assessment_clo_bp.route('/component/<int:component_id>', methods=['GET'])
@inject
def list_clos(component_id: int, service: AssessmentCloService = Provide[Container.assessment_clo_service]):
    items = service.get_clos_for_component(component_id)
    return jsonify([{'id': c.id, 'code': c.code, 'description': c.description} for c in items]), 200

@assessment_clo_bp.route('/', methods=['POST'])
@inject
def add_mapping(service: AssessmentCloService = Provide[Container.assessment_clo_service]):
    data = request.get_json() or {}
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    try:
        mapping = service.add_mapping(data['assessment_component_id'], data['syllabus_clo_id'])
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'assessment_component_id': mapping.assessment_component_id, 'syllabus_clo_id': mapping.syllabus_clo_id}), 201

@assessment_clo_bp.route('/', methods=['DELETE'])
@inject
def remove_mapping(service: AssessmentCloService = Provide[Container.assessment_clo_service]):
    data = request.get_json() or {}
    if not data:
        return jsonify({'error': 'Provide JSON body with assessment_component_id and syllabus_clo_id'}), 400
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    ok = service.remove_mapping(data['assessment_component_id'], data['syllabus_clo_id'])
    if not ok:
        return jsonify({'message': 'Mapping not found'}), 404
    return '', 204