from flask import Blueprint, jsonify
from src.models.country import Country
from src.models.city import City

countries_bp = Blueprint('countries_bp', __name__)

@countries_bp.route('/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    return jsonify([country.to_dict() for country in countries]), 200

@countries_bp.route('/countries/<country_code>', methods=['GET'])
def get_country_by_code(country_code):
    country = Country.query.filter_by(code=country_code).first()
    if not country:
        return jsonify({"msg": "Country not found"}), 404
    return jsonify(country.to_dict()), 200

@countries_bp.route('/countries/<country_code>/cities', methods=['GET'])
def get_country_cities(country_code):
    country = Country.query.filter_by(code=country_code).first()
    if not country:
        return jsonify({"msg": "Country not found"}), 404
    cities = City.query.filter_by(country_id=country.id).all()
    return jsonify([city.to_dict() for city in cities]), 200

