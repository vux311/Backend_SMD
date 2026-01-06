from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.syllabus_service import SyllabusService
from api.schemas.syllabus_schema import SyllabusSchema

syllabus_bp = Blueprint('syllabus', __name__, url_prefix='/syllabuses')

schema = SyllabusSchema()

@syllabus_bp.route('/', methods=['GET'])
@inject
def list_syllabuses(syllabus_service: SyllabusService = Provide[Container.syllabus_service]):
    """List syllabuses
    ---
    get:
      summary: List syllabuses
      tags:
        - Syllabuses
      responses:
        200:
          description: List of syllabuses
    """
    items = syllabus_service.list_syllabuses()
    return jsonify(schema.dump(items, many=True)), 200

@syllabus_bp.route('/<int:id>', methods=['GET'])
@inject
def get_syllabus(id: int, syllabus_service: SyllabusService = Provide[Container.syllabus_service]):
    """Get syllabus
    ---
    get:
      summary: Get syllabus by id
      tags:
        - Syllabuses
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Syllabus object
        404:
          description: Not found
    """
    s = syllabus_service.get_syllabus(id)
    if not s:
        return jsonify({'message': 'Syllabus not found'}), 404
    return jsonify(schema.dump(s)), 200

@syllabus_bp.route('/', methods=['POST'])
@inject
def create_syllabus(syllabus_service: SyllabusService = Provide[Container.syllabus_service]):
    """Create a syllabus
    ---
    post:
      summary: Create syllabus
      tags:
        - Syllabuses
      requestBody:
        required: true
      responses:
        201:
          description: Created
        400:
          description: Invalid input
    """
    data = request.get_json() or {}
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    try:
        s = syllabus_service.create_syllabus(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(schema.dump(s)), 201

@syllabus_bp.route('/<int:id>', methods=['PUT'])
@inject
def update_syllabus(id: int, syllabus_service: SyllabusService = Provide[Container.syllabus_service]):
    data = request.get_json() or {}
    errors = schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    s = syllabus_service.update_syllabus(id, data)
    if not s:
        return jsonify({'message': 'Syllabus not found'}), 404
    return jsonify(schema.dump(s)), 200

@syllabus_bp.route('/<int:id>', methods=['DELETE'])
@inject
def delete_syllabus(id: int, syllabus_service: SyllabusService = Provide[Container.syllabus_service]):
    ok = syllabus_service.delete_syllabus(id)
    if not ok:
        return jsonify({'message': 'Syllabus not found'}), 404
    return '', 204