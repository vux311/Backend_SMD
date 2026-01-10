from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.user_service import UserService
from api.schemas.user_schema import UserSchema
from api.middleware import token_required

user_bp = Blueprint('user', __name__, url_prefix='/users')

schema = UserSchema()

@user_bp.route('/', methods=['GET'])
@inject
def list_users(user_service: UserService = Provide[Container.user_service]):
    """Get all users
    ---
    get:
      summary: Get all users
      tags:
        - Users
      responses:
        200:
          description: List of users
    """
    users = user_service.list_users()
    return jsonify(schema.dump(users, many=True)), 200

@user_bp.route('/<int:id>', methods=['GET'])
@inject
def get_user(id: int, user_service: UserService = Provide[Container.user_service]):
    """Get user by id
    ---
    get:
      summary: Get user by ID
      tags:
        - Users
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: User object
        404:
          description: Not found
    """
    user = user_service.get_user(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(schema.dump(user)), 200


@user_bp.route('/me', methods=['GET'])
@inject
@token_required
def get_me(user_service: UserService = Provide[Container.user_service]):
    """Get current user from token
    """
    from flask import request
    payload = getattr(request, 'user', None)
    if not payload:
        return jsonify({'message': 'User not found in token'}), 404
    user_id = payload.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id missing in token'}), 400
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(schema.dump(user)), 200

@user_bp.route('/', methods=['POST'])
@inject
def create_user(user_service: UserService = Provide[Container.user_service]):
    """Create a new user
    ---
    post:
      summary: Create a new user
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      responses:
        201:
          description: User created
        400:
          description: Invalid input
    """
    data = request.get_json() or {}
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = user_service.create_user(data)
    return jsonify(schema.dump(user)), 201

@user_bp.route('/<int:id>', methods=['PUT'])
@inject
def update_user(id: int, user_service: UserService = Provide[Container.user_service]):
    """Update an existing user
    ---
    put:
      summary: Update user
      tags:
        - Users
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      responses:
        200:
          description: User updated
        400:
          description: Invalid input
        404:
          description: User not found
    """
    data = request.get_json() or {}
    errors = schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    user = user_service.update_user(id, data)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(schema.dump(user)), 200