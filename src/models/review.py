from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src import db
from src.models.review import Review
from src.models.user import User
from src.models.place import Place

reviews_bp = Blueprint('reviews_bp', __name__)

@reviews_bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_review = Review(
        user_id=user_id,
        place_id=data['place_id'],
        comment=data['comment'],
        rating=data['rating']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.to_dict()), 201

@reviews_bp.route('/reviews/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    claims = get_jwt()
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"msg": "Review not found"}), 404

    if not claims.get('is_admin') and review.user_id != get_jwt_identity():
        return jsonify({"msg": "Administration rights required"}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({"msg": "Review deleted"}), 200

@reviews_bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews]), 200

@reviews_bp.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"msg": "Review not found"}), 404
    return jsonify(review.to_dict()), 200

@reviews_bp.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_from_place(place_id):
    reviews = Review.query.filter_by(place_id=place_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

@reviews_bp.route('/users/<user_id>/reviews', methods=['GET'])
def get_reviews_from_user(user_id):
    reviews = Review.query.filter_by(user_id=user_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

@reviews_bp.route('/reviews/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    claims = get_jwt()
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"msg": "Review not found"}), 404

    if not claims.get('is_admin') and review.user_id != get_jwt_identity():
        return jsonify({"msg": "Administration rights required"}), 403

    data = request.get_json()
    review.comment = data.get('comment', review.comment)
    review.rating = data.get('rating', review.rating)
    db.session.commit()
    return jsonify(review.to_dict()), 200

