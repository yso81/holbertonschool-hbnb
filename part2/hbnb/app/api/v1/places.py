#!/usr/bin/python3
import sys
import os
from flask_restx import Namespace, Resource, fields
from app.api.v1.users import user_details_model
from app.api.v1.amenities import amenity_model

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)
from app.services import facade

api = Namespace('places', description='Place operations')


# This model is for creating/updating a place
place_input_model = api.model('PlaceInput', {
    'name': fields.String(required=True, description='Name of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'address': fields.String(required=True, description='Address of the place'),
    'city_id': fields.String(required=True, description='City ID'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'user_id': fields.String(required=True, description='The owner\'s user ID'),
    'number_of_rooms': fields.Integer(required=True, description='Number of rooms'),
    'bathrooms': fields.Integer(required=True, description='Number of bathrooms'),
    'price': fields.Float(required=True, description='Price per night'),
    'max_guests': fields.Integer(required=True, description='Maximum number of guests'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs')
})

# This model is for displaying place details
place_details_model = api.inherit('PlaceDetails', place_input_model, {
    'id': fields.String(readonly=True, description='The place unique identifier'),
    'owner': fields.Nested(user_details_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities')
})


@api.route('/')
class PlaceList(Resource):
    
    @api.doc('list_places')
    @api.marshal_list_with(place_details_model)
    def get(self):
        """List all places"""
        return facade.get_all_places()

    @api.doc('create_place')
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_details_model, code=201)
    def post(self):
        """Create a new place"""
        try:
            place_data = api.payload
            new_place = facade.create_place(place_data)
            return new_place, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    
    @api.doc('get_place_details')
    @api.marshal_with(place_details_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID '{place_id}' not found")
        return place

    @api.doc('update_place')
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_details_model)
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place's details"""
        try:
            update_data = api.payload
            updated_place = facade.update_place(place_id, update_data)
            if not updated_place:
                api.abort(404, f"Place with ID '{place_id}' not found")
            return updated_place
        except ValueError as e:
            api.abort(400, str(e))