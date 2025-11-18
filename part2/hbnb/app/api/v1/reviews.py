import re
from flask import request
from flask_restx import Namespace, Resource, fields, abort
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()

UUID_REGEX = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')

review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='The review unique identifier', pattern=UUID_REGEX.pattern),
    'user_id': fields.String(required=True, description='The user ID', pattern=UUID_REGEX.pattern),
    'place_id': fields.String(required=True, description='The place ID', pattern=UUID_REGEX.pattern),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5', min=1, max=5),
    'comment': fields.String(required=True, description='The review comment', min_length=1),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

review_input_model = api.model('ReviewInput', {
    'user_id': fields.String(required=True, description='The user ID of the reviewer', pattern=UUID_REGEX.pattern),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5', min=1, max=5),
    'comment': fields.String(required=True, description='The review text', min_length=1)
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(description='New rating (1-5)', min=1, max=5),
    'comment': fields.String(description='New comment text', min_length=1, max_length=1000)
})


@api.route('/places/<string:place_id>/reviews')
@api.param('place_id', 'The ID of the place being reviewed')
class ReviewList(Resource):
    """
    Handles creation and retrieval of reviews for a specific place
    """

    @api.doc('list_reviews_for_place')
    @api.marshal_list_with(review_model)
    @api.response(400, 'Invalid place ID format')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieves all reviews for a specific place
        """
        if not UUID_REGEX.match(place_id):
            api.abort(400, "Invalid place ID format. Must be a UUID.")

        # Validate place_id existence (optional, if you want to abort if place doesn't exist)
        if not facade.get_place(place_id): # Assuming facade has a get_place method
            api.abort(404, f"Place with ID '{place_id}' not found.")

        try:
            reviews = facade.get_reviews_for_place(place_id)
            return [review.to_dict() for review in reviews]
        except ValueError as e:
            api.abort(404, str(e))

    @api.doc('create_review')
    @api.expect(review_input_model, validate=True)
    @api.marshal_with(review_model, code=201)
    @api.response(400, 'Invalid input data or ID format')
    @api.response(404, 'User or Place not found')
    @api.response(409, 'Review by this user for this place already exists')
    def post(self, place_id):
        """
        Create a new review for a specific place
        """
        if not UUID_REGEX.match(place_id):
            api.abort(400, "Invalid place ID format. Must be a UUID.")

        data = api.payload
        data['place_id'] = place_id  # Add place_id from URL to the data
        
        user_id = data.get('user_id')
        if not facade.get_user(user_id): # Assuming facade has a get_user method
            api.abort(404, f"User with ID '{user_id}' not found.")
        
        if not facade.get_place(place_id): # Assuming facade has a get_place method
            api.abort(404, f"Place with ID '{place_id}' not found.")
        
        if facade.get_review_by_user_and_place(user_id, place_id): 
             api.abort(409, f"User '{user_id}' has already reviewed place '{place_id}'.")
        
        try:
            new_review = facade.create_review(data)
            return new_review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/reviews/<string:review_id>')
@api.param('review_id', 'The review identifier')
@api.response(400, 'Invalid review ID format')
@api.response(404, 'Review not found')
class ReviewResource(Resource):
    """
    Handles operations on a single review (get, update, delete)
    """

    @api.doc('get_review')
    @api.marshal_with(review_model)
    def get(self, review_id):
        """
        Retrieves a single review by its unique ID
        """
        if not UUID_REGEX.match(review_id):
            api.abort(400, "Invalid review ID format. Must be a UUID.")
        
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict()

    @api.doc('update_review')
    @api.expect(review_update_model, validate=True)
    @api.marshal_with(review_model)
    @api.response(400, 'Invalid input data or review ID format')

    def put(self, review_id):
        """
        Update an existing review's rating or comment
        """
        if not UUID_REGEX.match(review_id):
            api.abort(400, "Invalid review ID format. Must be a UUID.")
        
        data = api.payload
        if not data:
            api.abort(400, "No update data provided.")
        
        try:
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                api.abort(404, "Review not found")
            return updated_review.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review')
    @api.response(204, 'Review successfully deleted')
    @api.response(400, 'Invalid review ID format')
    def delete(self, review_id):
        """
        Deletes a review by its ID
        """
        if not UUID_REGEX.match(review_id):
            api.abort(400, "Invalid review ID format. Must be a UUID.")
        
        if facade.delete_review(review_id):
            return '', 204
        api.abort(404, "Review not found")
