from flask import Blueprint, request, jsonify
from flask_login import login_required
from ..models.student import Student
from ..extensions import db

api_students_bp = Blueprint('api_students', __name__)


# GET all students
@api_students_bp.route('/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([
        {"id": s.id, "name": s.name, "email": s.email}
        for s in students
    ])


 
@api_students_bp.route('/', methods=['POST'])
@login_required
def create_student():
    data = request.get_json()
    s = Student(name=data['name'], email=data.get('email'))
    db.session.add(s)
    db.session.commit()
    return jsonify({"id": s.id}), 201


 
@api_students_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()

    student.name = data['name']
    student.email = data.get('email')

    db.session.commit()
    return jsonify({"message": "Student updated"})


 
@api_students_bp.route('/<int:id>', methods=['PATCH'])
@login_required
def patch_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()

    if 'name' in data:
        student.name = data['name']
    if 'email' in data:
        student.email = data['email']

    db.session.commit()
    return jsonify({"message": "Student patched"})


 
@api_students_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Deleted"})
