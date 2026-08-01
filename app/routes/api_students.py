from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.student import Student

api_students_bp = Blueprint("api_students", __name__, url_prefix="/api")


# ✅ GET all students
@api_students_bp.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200


# ✅ GET single student
@api_students_bp.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student.to_dict()), 200


# ✅ POST create student
@api_students_bp.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    student = Student(name=name, email=email)
    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created",
        "student": student.to_dict()
    }), 201


# ✅ PUT update student
@api_students_bp.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    student.name = data.get("name", student.name)
    student.email = data.get("email", student.email)

    db.session.commit()

    return jsonify({
        "message": "Student updated",
        "student": student.to_dict()
    }), 200


# ✅ DELETE student
@api_students_bp.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted"}), 200