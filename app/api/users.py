from flask import Blueprint, request, jsonify, abort
from ..models.user import User
from ..extensions import db

api_users_bp = Blueprint('api_users', __name__)

@api_users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])

@api_users_bp.route('/', methods=['POST'])
def create_user():
    data = request.json or {}
    if 'username' not in data or 'password' not in data:
        abort(400)
    u = User(username=data['username'])
    u.set_password(data['password'])
    db.session.add(u)
    db.session.commit()
    return jsonify({'id': u.id, 'username': u.username}), 201
