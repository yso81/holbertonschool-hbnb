#!/usr/bin/python3
import sys
import os
import re
from flask_restx import Namespace, Resource, fields, abort
from app.api.v1.users import user_details_model
from app.api.v1.amenities import amenity_model

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)
from app.services import facade

api = Namespace('places', description='Place operations')

UUID_REGEX = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


# This model is for creating/updating a place
place_input_model = api.model('PlaceInput', {
    'name': fields.String(required=True, description='Name of the place', min_length=1),
    'description': fields.String(required=True, description='Description of the place', min_length=1),
    'address': fields.String(required=True, description='Address of the place', min_length=1),
    'latitude': fields.Float(required=True, description='Latitude of the place', min=-90.0, max=90.0),
    'longitude': fields.Float(required=True, description='Longitude of the place', min=-180.0, max=180.0),
    'user_id': fields.String(required=True, description='The owner\'s user ID', pattern=UUID_REGEX.pattern),
    'number_of_rooms': fields.Integer(required=True, description='Number of rooms', min=1),
    'bathrooms': fields.Integer(required=True, description='Number of bathrooms', min=0),
    'price': fields.Float(required=True, description='Price per night', min=0.01),
    'max_guests': fields.Integer(required=True, description='Maximum number of guests', min=1),
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
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Related resource not found (User, City, or Amenity)')
    def post(self):
        """
        Create a new place
        """
        place_data = api.payload

        if not facade.get_user(place_data['user_id']):
            api.abort(404, f"User with ID '{place_data['user_id']}' not found. Cannot create place.")
        
        if place_data.get('amenity_ids'):
            for amenity_id in place_data['amenity_ids']:
                if not facade.get_amenity(amenity_id):
                    api.abort(404, f"Amenity with ID '{amenity_id}' not found. Cannot create place.")
        
        try:
            new_place = facade.create_place(place_data)
            return new_place, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    
    @api.doc('get_place_details')
    @api.marshal_with(place_details_model)
    @api.response(400, 'Invalid place ID format')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID
        """
        if not UUID_REGEX.match(place_id):
            api.abort(400, "Invalid place ID format. Must be a UUID.")

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID '{place_id}' not found")
        return place

    @api.doc('update_place')
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_details_model)
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """
        Update a place's details
        """
        if not UUID_REGEX.match(place_id):
            api.abort(400, "Invalid place ID format. Must be a UUID.")
        
        update_data = api.payload

        if 'user_id' in update_data and not facade.get_user(update_data['user_id']):
            api.abort(404, f"User with ID '{update_data['user_id']}' not found. Cannot update place.")
        

        try:
            updated_place = facade.update_place(place_id, update_data)
            if not updated_place:
                api.abort(404, f"Place with ID '{place_id}' not found")
            return updated_place
        except ValueError as e:
            api.abort(400, str(e))