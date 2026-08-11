from flask import Flask
from .extensions import db, login_manager

def create_app(test_config=None):
    app=Flask(__name__)
    app.config.update(
        SECRET_KEY="secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.students import student_bp
    from .routes.courses import course_bp
    from .api.enrollment import enrollment_bp
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(enrollment_bp)

    from .commands import register_commands
    register_commands(app)
    return app
