#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')


review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='The review identifier'),
    'text': fields.String(required=True, description='The review text'),
    'rating': fields.Integer(required=True, description='The rating (1-5)'),
    'user_id': fields.String(readonly=True, description='The user identifier'),
    'place_id': fields.String(required=True, description='The place identifier'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='The review text'),
    'rating': fields.Integer(required=True, description='The rating (1-5)', min=1, max=5),
    'place_id': fields.String(required=True, description='The place identifier')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='The review text'),
    'rating': fields.Integer(description='The rating (1-5)', min=1, max=5)
})

@api.route('/')
class ReviewList(Resource):
    
    @api.doc('create_review', security='Bearer Auth')
    @api.expect(review_input_model, validate=True)
    @api.marshal_with(review_model, code=201)
    @api.response(400, 'Invalid input')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Place not found')
    @api.response(409, 'Review already exists')
    @jwt_required()
    def post(self):
        """Create a new review"""
        current_user_id = get_jwt_identity()
        data = api.payload
        
        place = facade.get_place(data['place_id'])
        if not place:
            api.abort(404, "Place not found")

        all_reviews = facade.get_all_reviews()
        for r in all_reviews:
            if r.place_id == data['place_id'] and r.user_id == current_user_id:
                api.abort(409, "You have already reviewed this place.")

        try:
            review_data = {
                'text': data['text'],
                'rating': data['rating'],
                'user_id': current_user_id,
                'place_id': data['place_id']
            }
            new_review = facade.create_review(review_data)
            return new_review, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_reviews')
    @api.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews()


@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    
    @api.doc('get_review')
    @api.marshal_with(review_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @api.doc('update_review', security='Bearer Auth')
    @api.expect(review_update_model)
    @api.marshal_with(review_model)
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")

        if review.user_id != current_user_id and not is_admin:
            api.abort(403, "You are not authorized to update this review")

        try:
            updated_review = facade.update_review(review_id, api.payload)
            return updated_review
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review', security='Bearer Auth')
    @api.response(204, 'Review deleted')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
            
        if review.user_id != current_user_id and not is_admin:
             api.abort(403, "You are not authorized to delete this review")

        facade.delete_review(review_id)
        return '', 204
