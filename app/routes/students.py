from flask import Blueprint

student_bp = Blueprint('students', __name__, url_prefix='/students')

@student_bp.route('/')
def list_students():
    return "Students UI"
