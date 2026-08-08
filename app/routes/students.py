from flask import Blueprint, render_template, request, redirect
from ..models.student import Student
from ..extensions import db

student_bp = Blueprint('students', __name__, url_prefix='/students')

@student_bp.route('/')
def list_students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@student_bp.route('/add', methods=['POST'])
def add_student():
    s = Student(name=request.form['name'], email=request.form['email'])
    db.session.add(s)
    db.session.commit()
    return redirect('/students/')
