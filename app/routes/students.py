from flask import Blueprint, render_template, request, redirect, url_for
from ..models.student import Student
from ..extensions import db

student_bp = Blueprint('students', __name__, url_prefix='/students')


 
@student_bp.route('/')
def list_students():
    students = Student.query.all()
    return render_template('students.html', students=students)


 
@student_bp.route('/add', methods=['POST'])
def add_student():
    s = Student(
        name=request.form['name'],
        email=request.form['email']
    )
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('students.list_students'))


 
@student_bp.route('/edit/<int:id>')
def edit_student(id):
    student = Student.query.get_or_404(id)
    return render_template('edit_student.html', student=student)


 
@student_bp.route('/update/<int:id>', methods=['POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    student.name = request.form['name']
    student.email = request.form['email']
    db.session.commit()
    return redirect(url_for('students.list_students'))


 
@student_bp.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students.list_students'))
