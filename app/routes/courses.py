from flask import Blueprint
courses_bp = Blueprint('courses', __name__)
@courses_bp.route('/courses')
def courses(): return 'Courses'
