"""
Users controller module
"""

from flask import abort, request, jsonify
from src.models.user import User
from src import db


def get_users():
    """Returns all users"""
    users = User.get_all()
    return jsonify([user.to_dict() for user in users]), 200


def create_user():
    """Creates a new user"""
    data = request.get_json()
    if not data:
        abort(400, "Invalid JSON data")

    try:
        user = User.create(data)
    except (KeyError, ValueError) as e:
        abort(400, str(e))

    return jsonify(user.to_dict()), 201

def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    user = User.get(user_id)
    if not user:
        abort(404, f"User with ID {user_id} not found")
    return jsonify(user.to_dict()), 200


def update_user(user_id: str):
    """Updates a user by ID"""
    data = request.get_json()
    if not data:
        abort(400, "Invalid JSON data")

    user = User.update(user_id, data)
    if not user:
        abort(404, f"User with ID {user_id} not found")
    return jsonify(user.to_dict()), 200


def delete_user(user_id: str):
    """Deletes a user by ID"""
    if not User.delete(user_id):
        abort(404, f"User with ID {user_id} not found")
    return "", 204
