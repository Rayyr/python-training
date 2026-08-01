from flask import Flask
from .extensions import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes.students import students_bp
    app.register_blueprint(students_bp)

    return app