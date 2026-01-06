from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.academic_year_service import AcademicYearService
from api.schemas.academic_year_schema import AcademicYearSchema

academic_year_bp = Blueprint('academic_year', __name__, url_prefix='/academic-years')

schema = AcademicYearSchema()

@academic_year_bp.route('/', methods=['GET'])
@inject
def list_academic_years(academic_year_service: AcademicYearService = Provide[Container.academic_year_service]):
    """Get all academic years
    ---
    get:
      summary: Get all academic years
      tags:
        - AcademicYears
      responses:
        200:
          description: List of academic years
    """
    items = academic_year_service.list_academic_years()
    return jsonify(schema.dump(items, many=True)), 200

@academic_year_bp.route('/', methods=['POST'])
@inject
def create_academic_year(academic_year_service: AcademicYearService = Provide[Container.academic_year_service]):
    """Create a new academic year
    ---
    post:
      summary: Create an academic year
      tags:
        - AcademicYears
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
    ay = academic_year_service.create_academic_year(data)
    return jsonify(schema.dump(ay)), 201

@academic_year_bp.route('/<int:id>', methods=['PUT'])
@inject
def update_academic_year(id: int, academic_year_service: AcademicYearService = Provide[Container.academic_year_service]):
    data = request.get_json() or {}
    errors = schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    ay = academic_year_service.update_academic_year(id, data)
    if not ay:
        return jsonify({'message': 'AcademicYear not found'}), 404
    return jsonify(schema.dump(ay)), 200

@academic_year_bp.route('/<int:id>', methods=['DELETE'])
@inject
def delete_academic_year(id: int, academic_year_service: AcademicYearService = Provide[Container.academic_year_service]):
    ok = academic_year_service.delete_academic_year(id)
    if not ok:
        return jsonify({'message': 'AcademicYear not found'}), 404
    return '', 204