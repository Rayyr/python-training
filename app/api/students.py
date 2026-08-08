from flask import Blueprint, request, jsonify, abort
from ..models.student import Student
from ..extensions import db

api_students_bp = Blueprint('api_students', __name__)

@api_students_bp.route('/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'email': s.email} for s in students])

@api_students_bp.route('/', methods=['POST'])
def create_student():
    data = request.json or {}
    if 'name' not in data:
        abort(400)
    s = Student(name=data['name'], email=data.get('email'))
    db.session.add(s)
    db.session.commit()
    return jsonify({'id': s.id}), 201
