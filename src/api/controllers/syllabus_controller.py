from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.syllabus_service import SyllabusService
from api.schemas.syllabus_schema import SyllabusSchema
from api.schemas.syllabus_detail_schema import SyllabusDetailSchema
from api.middleware import token_required

syllabus_bp = Blueprint('syllabus', __name__, url_prefix='/syllabuses')

schema = SyllabusSchema()
detail_schema = SyllabusDetailSchema()

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


@syllabus_bp.route('/<int:id>/details', methods=['GET'])
@inject
def get_syllabus_details(id: int, syllabus_service: SyllabusService = Provide[Container.syllabus_service]):
    """Get full syllabus details
    ---
    get:
      summary: Get syllabus details by id
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
          description: Syllabus detail object
        404:
          description: Not found
    """
    s = syllabus_service.get_syllabus_details(id)
    if not s:
        return jsonify({'message': 'Syllabus not found'}), 404
    return jsonify(detail_schema.dump(s)), 200


@syllabus_bp.route('/<int:id>/submit', methods=['POST'])
@inject
def submit_syllabus(id: int, syllabus_service: SyllabusService = Provide[Container.syllabus_service]):
    """Submit a syllabus for evaluation
    ---
    post:
      summary: Submit syllabus
      tags:
        - Syllabuses
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
      responses:
        200:
          description: Submitted syllabus
        400:
          description: Invalid action
        404:
          description: Not found
    """
    data = request.get_json() or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id is required'}), 400
    try:
        s = syllabus_service.submit_syllabus(id, user_id)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    if not s:
        return jsonify({'message': 'Syllabus not found'}), 404
    return jsonify(schema.dump(s)), 200


@syllabus_bp.route('/<int:id>/evaluate', methods=['POST'])
@inject
def evaluate_syllabus(id: int, syllabus_service: SyllabusService = Provide[Container.syllabus_service]):
    """Evaluate (approve/reject) a syllabus
    ---
    post:
      summary: Evaluate syllabus
      tags:
        - Syllabuses
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
      responses:
        200:
          description: Evaluation result
        400:
          description: Invalid action or missing comment
        404:
          description: Not found
    """
    data = request.get_json() or {}
    action = data.get('action')
    user_id = data.get('user_id')
    comment = data.get('comment')
    if not action or not user_id:
        return jsonify({'message': 'action and user_id are required'}), 400
    try:
        s = syllabus_service.evaluate_syllabus(id, user_id, action, comment)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    if not s:
        return jsonify({'message': 'Syllabus not found'}), 404
    return jsonify(schema.dump(s)), 200


@syllabus_bp.route('/<int:id>/workflow-logs', methods=['GET'])
@inject
def get_workflow_logs(id: int, syllabus_service: SyllabusService = Provide[Container.syllabus_service]):
    """Get workflow logs for a syllabus
    ---
    get:
      summary: Get workflow logs
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
          description: List of workflow logs
        404:
          description: Not found
    """
    logs = syllabus_service.get_workflow_logs(id)
    from api.schemas.workflow_log_schema import WorkflowLogSchema
    schema_w = WorkflowLogSchema()
    return jsonify(schema_w.dump(logs, many=True)), 200

@syllabus_bp.route('/', methods=['POST'])
@inject
@token_required
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