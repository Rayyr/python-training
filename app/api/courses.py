from flask import Blueprint, request, jsonify
from flask_login import login_required
from ..models.course import Course
from ..extensions import db

api_courses_bp = Blueprint('api_courses', __name__)


@api_courses_bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{"id": c.id, "title": c.title} for c in courses])


@api_courses_bp.route('/', methods=['POST'])
@login_required
def create_course():
    data = request.get_json()
    c = Course(title=data['title'])
    db.session.add(c)
    db.session.commit()
    return jsonify({"id": c.id}), 201


@api_courses_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    course.title = data['title']
    db.session.commit()
    return jsonify({"message": "Updated"})


@api_courses_bp.route('/<int:id>', methods=['PATCH'])
@login_required
def patch_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()

    if 'title' in data:
        course.title = data['title']

    db.session.commit()
    return jsonify({"message": "Patched"})


@api_courses_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Deleted"})
