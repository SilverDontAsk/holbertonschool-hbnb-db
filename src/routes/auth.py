from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User
from src import bcrypt, db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 409

    # Create new user
    new_user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.email)
    return jsonify(access_token=access_token), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if user and bcrypt.check_password_hash(user.password_hash, data.get('password')):
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200