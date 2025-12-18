#!/usr/bin/python3
import sys
import os
import re
from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.api.v1.users import user_details_model
from app.api.v1.amenities import amenity_model
from app.api.v1.reviews import review_model

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)
from app.services import facade

api = Namespace('places', description='Place operations')

UUID_REGEX = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')

# --- MODELS ---

place_input_model = api.model('PlaceInput', {
    'name': fields.String(required=True, description='Name of the place', min_length=1),
    'description': fields.String(required=True, description='Description of the place', min_length=1),
    'address': fields.String(required=True, description='Address of the place', min_length=1),
    'city_name': fields.String(required=True, description='Name of the city'), 
    'latitude': fields.Float(required=True, description='Latitude of the place', min=-90.0, max=90.0),
    'longitude': fields.Float(required=True, description='Longitude of the place', min=-180.0, max=180.0),
    'number_of_rooms': fields.Integer(required=True, attribute='number_rooms', description='Number of rooms', min=1),
    'bathrooms': fields.Integer(required=True, attribute='number_bathrooms', description='Number of bathrooms', min=0),
    'price': fields.Float(required=True, attribute='price_by_night', description='Price per night', min=0.01),
    'max_guests': fields.Integer(required=True, attribute='max_guest', description='Maximum number of guests', min=1),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs')
})

place_details_model = api.inherit('PlaceDetails', place_input_model, {
    'id': fields.String(readonly=True, description='The place unique identifier'),
    'owner_id': fields.String(readonly=True, attribute='user_id', description='The Owner ID'),
    'city_id': fields.String(readonly=True, description='The City ID'), # <--- ADDED THIS
    'owner': fields.Nested(user_details_model, attribute='user', description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities')
})


@api.route('/')
class PlaceList(Resource):
    
    @api.doc('list_places')
    @api.marshal_list_with(place_details_model)
    def get(self):
        """List all places"""
        return facade.get_all_places()

    @api.doc('create_place', security='Bearer Auth')
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_details_model, code=201)
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Related resource not found (Amenity or City)')
    @jwt_required()
    def post(self):
        """
        Create a new place (Authenticated)
        """
        current_user_id = get_jwt_identity()
        place_data = api.payload

        if place_data.get('city_id'):
            if hasattr(facade, 'get_city') and not facade.get_city(place_data['city_id']):
                api.abort(404, f"City with ID '{place_data['city_id']}' not found.")

        creation_data = {
            'name': place_data['name'],
            'description': place_data['description'],
            'address': place_data.get('address'),
            'city_id': place_data.get('city_id'),
            'price_by_night': place_data['price'],
            'number_rooms': place_data['number_of_rooms'],
            'number_bathrooms': place_data['bathrooms'],
            'max_guest': place_data['max_guests'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude'],
            'user_id': current_user_id
        }

        if place_data.get('amenity_ids'):
            for amenity_id in place_data['amenity_ids']:
                if not facade.get_amenity(amenity_id):
                    api.abort(404, f"Amenity with ID '{amenity_id}' not found. Cannot create place.")
        
        try:
            new_place = facade.create_place(creation_data)
            
            if place_data.get('amenity_ids'):
                for amenity_id in place_data['amenity_ids']:
                    amenity = facade.get_amenity(amenity_id)
                    if amenity:
                        new_place.add_amenity(amenity)

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

    @api.doc('update_place', security='Bearer Auth')
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_details_model)
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - You do not own this place')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """
        Update a place's details (Owner or Admin only)
        """
        if not UUID_REGEX.match(place_id):
            api.abort(400, "Invalid place ID format. Must be a UUID.")
        
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID '{place_id}' not found")

        place_owner_id = place.user_id if hasattr(place, 'user_id') else getattr(place, 'owner_id', None)
        
        if str(place_owner_id) != str(current_user_id) and not is_admin:
            api.abort(403, "You are not authorized to modify this place.")

        update_data = api.payload
        
        if 'user_id' in update_data:
            del update_data['user_id']

        try:
            updated_place = facade.update_place(place_id, update_data)
            return updated_place
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_place', security='Bearer Auth')
    @api.response(204, 'Place deleted successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - You do not own this place')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """
        Delete a place (Owner or Admin only)
        """
        if not UUID_REGEX.match(place_id):
            api.abort(400, "Invalid place ID format. Must be a UUID.")
        
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID '{place_id}' not found")

        place_owner_id = place.user_id if hasattr(place, 'user_id') else getattr(place, 'owner_id', None)
        
        if str(place_owner_id) != str(current_user_id) and not is_admin:
            api.abort(403, "You are not authorized to delete this place.")

        if hasattr(facade, 'delete_place'):
             facade.delete_place(place_id)
        elif hasattr(facade, 'place_repo'):
             facade.place_repo.delete(place_id)
        else:
             api.abort(500, "Server configuration error: cannot delete place.")

        return '', 204


@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.doc('get_place_amenities')
    @api.marshal_list_with(amenity_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all amenities for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        
        return place.amenities


@api.route('/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.doc('get_place_reviews')
    @api.marshal_list_with(review_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
            
        all_reviews = facade.get_all_reviews()
        place_reviews = [r for r in all_reviews if r.place_id == place_id]
        
        return place_reviews
