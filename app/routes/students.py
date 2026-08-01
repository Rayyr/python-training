from flask import Blueprint, render_template, request, redirect
from ..extensions import db
from ..models.student import Student

students_bp = Blueprint('students', __name__)

@students_bp.route('/')
def home():
    return render_template('home.html')

@students_bp.route('/students')
def students():
    all_students = Student.query.all()
    return render_template('students.html', students=all_students)

@students_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        student = Student(name=name, email=email)
        db.session.add(student)
        db.session.commit()

        return redirect('/students')

    return render_template('register.html')