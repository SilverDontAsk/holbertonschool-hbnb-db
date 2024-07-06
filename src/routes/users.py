from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.models.user import User
from src import db, bcrypt

def register():
    users_bp = Blueprint('users_bp', __name__)

    @users_bp.route('/users', methods=['POST'])
    @jwt_required()
    def create_user():
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({"msg": "Administration rights required"}), 403

        data = request.get_json()
        new_user = User(
            email=data['email'],
            password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_admin=data.get('is_admin', False)
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

    @users_bp.route('/users/<int:user_id>', methods=['DELETE'])
    @jwt_required()
    def delete_user(user_id):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({"msg": "Administration rights required"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted"}), 200

    @users_bp.route('/users/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_user_by_id(user_id):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({"msg": "Administration rights required"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        return jsonify(user.to_dict()), 200

    @users_bp.route('/users', methods=['GET'])
    @jwt_required()
    def get_users():
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({"msg": "Administration rights required"}), 403

        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200

    @users_bp.route('/users/<int:user_id>', methods=['PUT'])
    @jwt_required()
    def update_user(user_id):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({"msg": "Administration rights required"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        data = request.get_json()
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.is_admin = data.get('is_admin', user.is_admin)
        db.session.commit()
        return jsonify(user.to_dict()), 200

    return users_bp
