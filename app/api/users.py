from flask import Blueprint, request, jsonify
from flask_login import login_required
from ..models.user import User
from ..extensions import db

api_users_bp = Blueprint('api_users', __name__)


@api_users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username} for u in users])


# PROTECT USER CREATION
@api_users_bp.route('/', methods=['POST'])
@login_required
def create_user():
    data = request.get_json()
    u = User(username=data['username'], password=data['password'])
    db.session.add(u)
    db.session.commit()
    return jsonify({"id": u.id}), 201


@api_users_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Deleted"})
