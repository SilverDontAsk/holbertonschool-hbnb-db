from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src import db
from src.models.place import Place

places_bp = Blueprint('places_bp', __name__)

@places_bp.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    data = request.get_json()
    new_place = Place(name=data['name'], description=data['description'], city_id=data['city_id'])
    db.session.add(new_place)
    db.session.commit()
    return jsonify(new_place.to_dict()), 201

@places_bp.route('/places/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    place = Place.query.get(place_id)
    if not place:
        return jsonify({"msg": "Place not found"}), 404

    db.session.delete(place)
    db.session.commit()
    return jsonify({"msg": "Place deleted"}), 200

@places_bp.route('/places', methods=['GET'])
def get_places():
    places = Place.query.all()
    return jsonify([place.to_dict() for place in places]), 200

@places_bp.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({"msg": "Place not found"}), 404
    return jsonify(place.to_dict()), 200

@places_bp.route('/places/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    place = Place.query.get(place_id)
    if not place:
        return jsonify({"msg": "Place not found"}), 404

    data = request.get_json()
    place.name = data.get('name', place.name)
    place.description = data.get('description', place.description)
    place.city_id = data.get('city_id', place.city_id)
    db.session.commit()
    return jsonify(place.to_dict()), 200
