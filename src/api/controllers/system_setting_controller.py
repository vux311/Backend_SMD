from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.system_setting_service import SystemSettingService
from api.schemas.system_setting_schema import SystemSettingSchema

system_setting_bp = Blueprint('system_setting', __name__, url_prefix='/system-settings')
schema = SystemSettingSchema()

@system_setting_bp.route('/', methods=['GET'])
@inject
def list_settings(service: SystemSettingService = Provide[Container.system_setting_service]):
    items = service.get_all_settings()
    return jsonify(schema.dump(items, many=True)), 200

@system_setting_bp.route('/', methods=['POST'])
@inject
def update_setting(service: SystemSettingService = Provide[Container.system_setting_service]):
    data = request.get_json() or {}
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    item = service.update_setting(data['key'], data['value'], data.get('description'))
    return jsonify(schema.dump(item)), 200