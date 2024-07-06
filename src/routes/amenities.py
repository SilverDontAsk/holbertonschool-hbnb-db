from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src import db
from src.models.amenity import Amenity

amenities_bp = Blueprint('amenities_bp', __name__)

@amenities_bp.route('/amenities', methods=['POST'])
@jwt_required()
def create_amenity():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    
    data = request.get_json()
    new_amenity = Amenity(name=data['name'])
    db.session.add(new_amenity)
    db.session.commit()
    return jsonify(new_amenity), 201

@amenities_bp.route('/amenities/<amenity_id>', methods=['DELETE'])
@jwt_required()
def delete_amenity(amenity_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        return jsonify({"msg": "Amenity not found"}), 404

    db.session.delete(amenity)
    db.session.commit()
    return jsonify({"msg": "Amenity deleted"}), 200


@amenities_bp.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = Amenity.query.all()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200

@amenities_bp.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        return jsonify({"msg": "Amenity not found"}), 404
    return jsonify(amenity.to_dict()), 200

@amenities_bp.route('/amenities/<amenity_id>', methods=['PUT'])
@jwt_required()
def update_amenity(amenity_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        return jsonify({"msg": "Amenity not found"}), 404

    data = request.get_json()
    amenity.name = data.get('name', amenity.name)
    db.session.commit()
    return jsonify(amenity.to_dict()), 200