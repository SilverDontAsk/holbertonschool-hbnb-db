from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src import db
from src.models.city import City
from src.models.country import Country

cities_bp = Blueprint('cities_bp', __name__)

@cities_bp.route('/cities', methods=['POST'])
@jwt_required()
def create_city():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    
    data = request.get_json()
    country = Country.query.get(data['country_id'])
    if not country:
        return jsonify({"msg": "Country not found"}), 404

    new_city = City(name=data['name'], country_id=data['country_id'])
    db.session.add(new_city)
    db.session.commit()
    return jsonify(new_city.to_dict()), 201

@cities_bp.route('/cities/<city_id>', methods=['DELETE'])
@jwt_required()
def delete_city(city_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    
    city = City.query.get(city_id)
    if not city:
        return jsonify({"msg": "City not found"}), 404

    db.session.delete(city)
    db.session.commit()
    return jsonify({"msg": "City deleted"}), 200

@cities_bp.route('/cities', methods=['GET'])
def get_cities():
    cities = City.query.all()
    return jsonify([city.to_dict() for city in cities]), 200

@cities_bp.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    city = City.query.get(city_id)
    if not city:
        return jsonify({"msg": "City not found"}), 404
    return jsonify(city.to_dict()), 200

@cities_bp.route('/cities/<city_id>', methods=['PUT'])
@jwt_required()
def update_city(city_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    city = City.query.get(city_id)
    if not city:
        return jsonify({"msg": "City not found"}), 404

    data = request.get_json()
    if 'country_id' in data:
        country = Country.query.get(data['country_id'])
        if not country:
            return jsonify({"msg": "Country not found"}), 404
        city.country_id = data['country_id']
    
    city.name = data.get('name', city.name)
    db.session.commit()
    return jsonify(city.to_dict()), 200
