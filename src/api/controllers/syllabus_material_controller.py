from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.syllabus_material_service import SyllabusMaterialService
from api.schemas.syllabus_material_schema import SyllabusMaterialSchema

syllabus_material_bp = Blueprint('syllabus_material', __name__, url_prefix='/syllabus-materials')

schema = SyllabusMaterialSchema()

@syllabus_material_bp.route('/syllabus/<int:syllabus_id>', methods=['GET'])
@inject
def list_materials(syllabus_id: int, syllabus_material_service: SyllabusMaterialService = Provide[Container.syllabus_material_service]):
    items = syllabus_material_service.get_by_syllabus(syllabus_id)
    return jsonify(schema.dump(items, many=True)), 200

@syllabus_material_bp.route('/', methods=['POST'])
@inject
def create_material(syllabus_material_service: SyllabusMaterialService = Provide[Container.syllabus_material_service]):
    data = request.get_json() or {}
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    try:
        item = syllabus_material_service.create_material(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(schema.dump(item)), 201

@syllabus_material_bp.route('/<int:id>', methods=['DELETE'])
@inject
def delete_material(id: int, syllabus_material_service: SyllabusMaterialService = Provide[Container.syllabus_material_service]):
    ok = syllabus_material_service.delete_material(id)
    if not ok:
        return jsonify({'message': 'Material not found'}), 404
    return '', 204