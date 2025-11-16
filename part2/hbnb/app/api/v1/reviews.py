from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()

review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='The review unique identifier'),
    'user_id': fields.String(required=True, description='The user ID'),
    'place_id': fields.String(required=True, description='The place ID'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'comment': fields.String(required=True, description='The review comment'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

review_input_model = api.model('ReviewInput', {
    'user_id': fields.String(required=True, description='The user ID of the reviewer'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5', min=1, max=5),
    'comment': fields.String(required=True, description='The review text')
})

@api.route('/places/<string:place_id>/reviews')
@api.param('place_id', 'The ID of the place being reviewed')
class ReviewList(Resource):
    """
    Handles creation and retrieval of reviews for a specific place
    """

    @api.doc('list_reviews_for_place')
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """
        Retrieves all reviews for a specific place
        """
        try:
            reviews = facade.get_reviews_for_place(place_id)
            return [review.to_dict() for review in reviews]
        except ValueError as e:
            api.abort(404, str(e))

    @api.doc('create_review')
    @api.expect(review_input_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self, place_id):
        """
        Create a new review for a specific place
        """
        data = request.json
        data['place_id'] = place_id  # Add place_id from URL to the data
        try:
            new_review = facade.create_review(data)
            return new_review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/reviews/<string:review_id>')
@api.param('review_id', 'The review identifier')
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
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict()

    @api.doc('update_review')
    @api.expect(api.model('ReviewUpdate', {
        'rating': fields.Integer(description='New rating (1-5)'),
        'comment': fields.String(description='New comment text')
    }))
    @api.marshal_with(review_model)
    def put(self, review_id):
        """
        Update an existing review's rating or comment
        """
        data = request.json
        try:
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                api.abort(404, "Review not found")
            return updated_review.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review')
    @api.response(204, 'Review successfully deleted')
    def delete(self, review_id):
        """
        Deletes a review by its ID
        """
        if facade.delete_review(review_id):
            return '', 204
        api.abort(404, "Review not found")
