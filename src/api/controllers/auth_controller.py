from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.user_service import UserService
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
@inject
def login(user_service: UserService = Provide[Container.user_service]):
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'username and password are required'}), 400
    user = user_service.get_by_username(username)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401
    if not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Get role name if available
    role_name = None
    try:
        if user.roles and len(user.roles) > 0 and getattr(user.roles[0], 'role', None):
            role_name = user.roles[0].role.name
    except Exception:
        role_name = None

    token = f"fake-jwt-token-for-{username}"
    return jsonify({'token': token, 'user_id': user.id, 'role': role_name}), 200