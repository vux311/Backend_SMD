from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.ai_service import AiService

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/generate', methods=['POST'])
@inject
def generate(ai_service: AiService = Provide[Container.ai_service]):
    data = request.get_json() or {}
    subject_name = data.get('subject_name')
    if not subject_name:
        return jsonify({'message': 'subject_name is required'}), 400

    res = ai_service.generate(subject_name)
    if isinstance(res, dict) and res.get('error'):
        return jsonify({'message': res.get('error')}), 500

    return jsonify(res), 200
