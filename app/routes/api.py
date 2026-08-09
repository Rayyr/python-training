from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models.course import Course

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.post("/courses/<int:course_id>/enroll")
@login_required
def enroll(course_id):
    if not current_user.has_role("student"):
        return jsonify({"error": "Only students can enroll themselves."}), 403

    if current_user.student is None:
        return jsonify({"error": "The current user is not linked to a student record."}), 400

    course = db.session.get(Course, course_id)
    if course is None:
        return jsonify({"error": "Course not found."}), 404

    if course in current_user.student.courses:
        return jsonify({
            "message": "Student is already enrolled.",
            "course_id": course.id,
            "student_id": current_user.student.id,
        }), 200

    current_user.student.courses.append(course)
    db.session.commit()

    return jsonify({
        "message": "Enrollment successful.",
        "course_id": course.id,
        "course_title": course.title,
        "student_id": current_user.student.id,
    }), 201

@api_bp.get("/courses/<int:course_id>/students")
@login_required
def course_students(course_id):
    course = db.session.get(Course, course_id)
    if course is None:
        return jsonify({"error": "Course not found."}), 404

    return jsonify({
        "course": {"id": course.id, "title": course.title},
        "students": [
            {"id": s.id, "name": s.name, "email": s.email}
            for s in course.students
        ],
    })
