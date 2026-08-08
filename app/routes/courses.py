from flask import Blueprint, render_template, request, redirect
from ..models.course import Course
from ..extensions import db

course_bp = Blueprint('courses', __name__, url_prefix='/courses')

@course_bp.route('/')
def list_courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@course_bp.route('/add', methods=['POST'])
def add_course():
    c = Course(title=request.form['title'])
    db.session.add(c)
    db.session.commit()
    return redirect('/courses/')
