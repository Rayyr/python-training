from flask import Flask
from .extensions import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    from .routes.api_students import api_students_bp
    app.register_blueprint(api_students_bp)

    return app