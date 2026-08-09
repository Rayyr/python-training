from flask import Blueprint, render_template, request, redirect, url_for
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
    return redirect(url_for('courses.list_courses'))


 
@course_bp.route('/edit/<int:id>')
def edit_course(id):
    course = Course.query.get_or_404(id)
    return render_template('edit_course.html', course=course)


 
@course_bp.route('/update/<int:id>', methods=['POST'])
def update_course(id):
    course = Course.query.get_or_404(id)
    course.title = request.form['title']
    db.session.commit()
    return redirect(url_for('courses.list_courses'))


 
@course_bp.route('/delete/<int:id>')
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('courses.list_courses'))
