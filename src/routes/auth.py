from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from src.models.user import User
from src import bcrypt, db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.email)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401
