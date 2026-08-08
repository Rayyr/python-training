from flask import Blueprint, request, jsonify, abort
from ..models.course import Course
from ..extensions import db

api_courses_bp = Blueprint('api_courses', __name__)

@api_courses_bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{'id': c.id, 'title': c.title} for c in courses])

@api_courses_bp.route('/', methods=['POST'])
def create_course():
    data = request.json or {}
    if 'title' not in data:
        abort(400)
    c = Course(title=data['title'])
    db.session.add(c)
    db.session.commit()
    return jsonify({'id': c.id}), 201
