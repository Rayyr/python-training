from flask import Flask
from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
    app.config["UPLOAD_FOLDER"] = "uploads/profile_pictures"
    app.config["ALLOWED_PROFILE_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .models.user import User
    from .models.student import Student
    from .models.course import Course

    from .routes.auth import auth_bp
    from .routes.students import student_bp
    from .routes.courses import course_bp
    from .routes.profile import profile_bp
    from .routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(api_bp)

    return app
