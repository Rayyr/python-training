from flask import Flask
from .extensions import db, login_manager

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.students import student_bp
    from .routes.courses import course_bp
    from .api.users import api_users_bp
    from .api.students import api_students_bp
    from .api.courses import api_courses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(api_users_bp, url_prefix="/api/users")
    app.register_blueprint(api_students_bp, url_prefix="/api/students")
    app.register_blueprint(api_courses_bp, url_prefix="/api/courses")

    return app
