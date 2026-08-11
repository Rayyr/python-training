from flask import Flask, render_template
from .extensions import db, login_manager
import os


def create_app(test_config=None):

    app = Flask(__name__)

    app.config.update(
        SECRET_KEY="dev-secret-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

        UPLOAD_FOLDER=os.path.join(
            app.root_path,
            "static",
            "uploads"
        )
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.students import student_bp
    from .routes.courses import course_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template(
            "404.html"
        ), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template(
            "500.html"
        ), 500

    with app.app_context():
        db.create_all()

    return app