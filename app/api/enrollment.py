from flask import Blueprint, request, jsonify
from flask_login import login_required

from ..models.student import Student
from ..models.course import Course
from ..extensions import db

enrollment_bp = Blueprint("enrollment", __name__, url_prefix="/api/enrollment")


@enrollment_bp.route("/", methods=["POST"])
@login_required
def enroll():
    data = request.get_json() or {}

    student = Student.query.get(data.get("student_id"))

    course = Course.query.get(data.get("course_id"))

    if not student or not course:
        return jsonify({"error": "Student or course not found"}), 404

    if course in student.courses:
        return jsonify({"error": "Already enrolled"}), 409

    student.courses.append(course)

    db.session.commit()

    return jsonify({"message": "Enrolled successfully"}), 201


@enrollment_bp.route("/student/<int:student_id>", methods=["GET"])
def student_courses(student_id):
    student = Student.query.get_or_404(student_id)

    return jsonify(
        [{"id": course.id, "title": course.title} for course in student.courses]
    )


@enrollment_bp.route(
    "/student/<int:student_id>/course/<int:course_id>", methods=["DELETE"]
)
@login_required
def remove_enrollment(student_id, course_id):
    student = Student.query.get_or_404(student_id)

    course = Course.query.get_or_404(course_id)

    if course not in student.courses:
        return jsonify({"error": "Enrollment not found"}), 404

    student.courses.remove(course)

    db.session.commit()

    return jsonify({"message": "Enrollment removed"})
