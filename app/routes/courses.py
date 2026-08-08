from flask import Blueprint

course_bp = Blueprint('courses', __name__, url_prefix='/courses')

@course_bp.route('/')
def list_courses():
    return "Courses UI"
