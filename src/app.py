from flask import Flask, jsonify
from api.swagger import spec
from api.middleware import middleware
from api.responses import success_response
from infrastructure.databases import init_db
from config import Config
from flasgger import Swagger
from config import SwaggerConfig
from flask_swagger_ui import get_swaggerui_blueprint
from cors import CORS

# Dependency injection
from dependency_container import Container
from api.controllers.subject_controller import subject_bp
from api.controllers.faculty_controller import faculty_bp
from api.controllers.department_controller import department_bp
from api.controllers.role_controller import role_bp
from api.controllers.user_controller import user_bp
from api.controllers.academic_year_controller import academic_year_bp
from api.controllers.program_controller import program_bp
from api.controllers.syllabus_controller import syllabus_bp


def create_app():
    app = Flask(__name__)
    Swagger(app)

    # Initialize DI container and wire controllers
    container = Container()
    # Wire the container explicitly for controllers
    try:
        container.wire(modules=[
            "api.controllers.subject_controller",
            "api.controllers.faculty_controller",
            "api.controllers.department_controller",
            "api.controllers.role_controller",
            "api.controllers.user_controller",
            "api.controllers.academic_year_controller",
            "api.controllers.program_controller",
        ])
    except Exception:
        # best-effort wiring; if it fails here the app can still start
        pass

    # Register blueprints
    app.register_blueprint(subject_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(academic_year_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(syllabus_bp)

     # Thêm Swagger UI blueprint
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Syllabus Management API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    try:
        init_db(app)
    except Exception as e:
        print(f"Error initializing database: {e}")

    # Register middleware
    middleware(app)

    # Register routes (add all non-static endpoints to Swagger where possible)
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':
                continue
            view_func = app.view_functions.get(rule.endpoint)
            if not view_func:
                continue
            try:
                spec.path(view=view_func)
                print(f"Adding path: {rule.rule} -> {view_func}")
            except Exception:
                # some endpoints may not be compatible with flasgger, skip them
                pass

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    return app
# Run the application

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9999, debug=True) 