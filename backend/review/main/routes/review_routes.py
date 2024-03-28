from flask import Flask, request, jsonify, Flask, Blueprint
from main.models.review_model import db, Review

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/reviews', methods=['POST'])
def create_review():
    review_data = request.get_json()
    new_review = Review(
        reviewer_id=review_data['reviewer_id'],
        reviewee_id=review_data['reviewee_id'],
        message=review_data['message'],
        rating=review_data['rating']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review created successfully', 'review': {
        'review_id': new_review.review_id,
        'reviewer_id': new_review.reviewer_id,
        'reviewee_id': new_review.reviewee_id,
        'message': new_review.message,
        'rating': new_review.rating,
        'created_at': new_review.created_at
    }}), 201

@review_bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    reviews_list = [{
        'review_id': review.review_id,
        'reviewer_id': review.reviewer_id,
        'reviewee_id': review.reviewee_id,
        'message': review.message,
        'rating': review.rating,
        'created_at': review.created_at
    } for review in reviews]
    return jsonify({'reviews': reviews_list})


@review_bp.route('/review/<int:reviewee_id>', methods=['GET'])
def get_review_by_reviewee(reviewee_id):
    reviews = Review.query.filter_by(reviewee_id=reviewee_id).all()
    reviews_list = [{
        'review_id': review.review_id,
        'reviewer_id': review.reviewer_id,
        'reviewee_id': review.reviewee_id,
        'message': review.message,
        'rating': review.rating,
        'created_at': review.created_at
    } for review in reviews]
    return jsonify({'reviews': reviews_list})