import os
from flask import Flask, render_template
from .extensions import db, login_manager


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.update(
        SECRET_KEY="dev-secret-change-me",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.path.join(
            os.path.dirname(__file__),
            "static",
            "uploads"
        ),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    from .models import user, student, course, enrollment

    from .routes.auth import auth_bp
    from .routes.students import student_bp
    from .routes.courses import course_bp
    from .api.enrollment import enrollment_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(enrollment_bp)

    register_error_handlers(app)

    return app


def register_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template("500.html"), 500
