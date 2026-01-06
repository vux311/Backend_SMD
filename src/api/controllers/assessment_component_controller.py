from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.assessment_component_service import AssessmentComponentService
from api.schemas.assessment_component_schema import AssessmentComponentSchema

assessment_component_bp = Blueprint('assessment_component', __name__, url_prefix='/assessment-components')

schema = AssessmentComponentSchema()

@assessment_component_bp.route('/', methods=['POST'])
@inject
def create_component(service: AssessmentComponentService = Provide[Container.assessment_component_service]):
    data = request.get_json() or {}
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    try:
        item = service.create_component(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(schema.dump(item)), 201

@assessment_component_bp.route('/<int:id>', methods=['PUT'])
@inject
def update_component(id: int, service: AssessmentComponentService = Provide[Container.assessment_component_service]):
    data = request.get_json() or {}
    errors = schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    item = service.update_component(id, data)
    if not item:
        return jsonify({'message': 'Component not found'}), 404
    return jsonify(schema.dump(item)), 200

@assessment_component_bp.route('/<int:id>', methods=['DELETE'])
@inject
def delete_component(id: int, service: AssessmentComponentService = Provide[Container.assessment_component_service]):
    ok = service.delete_component(id)
    if not ok:
        return jsonify({'message': 'Component not found'}), 404
    return '', 204