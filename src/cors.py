from flask_cors import CORS

def init_cors(app):
    # Restrict origins to the frontend (Next.js dev host) and allow Authorization header
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000"],
            "allow_headers": ["Authorization", "Content-Type"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        }
    }, supports_credentials=True)
    app.config.setdefault('CORS_HEADERS', 'Content-Type')
    return app