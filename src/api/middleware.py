# Middleware functions for processing requests and responses

from flask import request, jsonify, current_app
from werkzeug.exceptions import HTTPException
import logging


def log_request_info(app):
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


def handle_options_request():
    return jsonify({'message': 'CORS preflight response'}), 200


def error_handling_middleware(error):
    # Preserve HTTPException responses (e.g., redirects, 404/405) instead of masking them
    if isinstance(error, HTTPException):
        return error

    # Log full exception traceback for diagnostics
    try:
        current_app.logger.exception('Unhandled exception during request')
    except Exception:
        logging.exception('Unhandled exception during request (logger unavailable)')

    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response

def add_custom_headers(response):
    response.headers['X-Custom-Header'] = 'Value'
    return response

from functools import wraps


def middleware(app):
    @app.before_request
    def before_request():
        log_request_info(app)

    @app.after_request
    def after_request(response):
        return add_custom_headers(response)

    @app.errorhandler(Exception)
    def handle_exception(error):
        return error_handling_middleware(error)

    @app.route('/options', methods=['OPTIONS'])
    def options_route():
        return handle_options_request()


# Simple token decorator for demo purposes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import request
        auth = request.headers.get('Authorization', '')
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'message': 'Authorization token is missing'}), 401
        token = auth.split(' ', 1)[1]
        # Very simple token check for demo
        if not token.startswith('fake-jwt-token'):
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)

    return decorated