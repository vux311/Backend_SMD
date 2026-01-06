from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.syllabus_clo_service import SyllabusCloService
from api.schemas.syllabus_clo_schema import SyllabusCloSchema

syllabus_clo_bp = Blueprint('syllabus_clo', __name__, url_prefix='/syllabus-clos')

schema = SyllabusCloSchema()

@syllabus_clo_bp.route('/syllabus/<int:syllabus_id>', methods=['GET'])
@inject
def list_clos(syllabus_id: int, syllabus_clo_service: SyllabusCloService = Provide[Container.syllabus_clo_service]):
    items = syllabus_clo_service.get_by_syllabus(syllabus_id)
    return jsonify(schema.dump(items, many=True)), 200

@syllabus_clo_bp.route('/', methods=['POST'])
@inject
def create_clo(syllabus_clo_service: SyllabusCloService = Provide[Container.syllabus_clo_service]):
    data = request.get_json() or {}
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    try:
        item = syllabus_clo_service.create_clo(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(schema.dump(item)), 201

@syllabus_clo_bp.route('/<int:id>', methods=['PUT'])
@inject
def update_clo(id: int, syllabus_clo_service: SyllabusCloService = Provide[Container.syllabus_clo_service]):
    data = request.get_json() or {}
    errors = schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    item = syllabus_clo_service.update_clo(id, data)
    if not item:
        return jsonify({'message': 'CLO not found'}), 404
    return jsonify(schema.dump(item)), 200

@syllabus_clo_bp.route('/<int:id>', methods=['DELETE'])
@inject
def delete_clo(id: int, syllabus_clo_service: SyllabusCloService = Provide[Container.syllabus_clo_service]):
    ok = syllabus_clo_service.delete_clo(id)
    if not ok:
        return jsonify({'message': 'CLO not found'}), 404
    return '', 204