#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields, abort
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='The unique identifier of an amenity'),
    'name': fields.String(required=True, description='Name of the amenity'),
    'created_at': fields.DateTime(readonly=True, description='The date and time the amenity was created'),
    'updated_at': fields.DateTime(readonly=True, description='The date and time the amenity was last updated'),
})

# Model for creating a new amenity
amenity_create_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Name of the amenity', min_length=1)
})


@api.route('/')
class AmenityList(Resource):
    @api.doc('create_amenity', security='Bearer Auth')
    @api.expect(amenity_create_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - Admin privileges required')
    @api.response(409, 'Amenity with this name already exists')
    @jwt_required()
    def post(self):
        """Register a new amenity (Admin only)"""
        # ADMIN CHECK
        claims = get_jwt()
        if not claims.get('is_admin'):
            api.abort(403, "Admin privileges required to create amenities.")

        data = api.payload

        name = data.get('name')
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            api.abort(400, "Amenity name cannot be empty or invalid.")
        
        try:
            new_amenity = facade.create_amenity(data)
            return new_amenity, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_list_with(amenity_model)
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return amenities, 200

@api.route('/<amenity_id>')
@api.param('amenity_id', 'The unique identifier of the amenity')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(400, 'Invalid amenity ID format')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID
        """
        if not amenity_id or not isinstance(amenity_id, str) or len(amenity_id.strip()) == 0:
            api.abort(400, "Amenity ID cannot be empty or invalid.")
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity with ID '{amenity_id}' not found")
        return amenity

    @api.doc('update_amenity', security='Bearer Auth')
    @api.expect(amenity_create_model, validate=True)
    @api.marshal_with(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - Admin privileges required')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Amenity with this name already exists')
    @jwt_required()
    def put(self, amenity_id):
        """
        Update an amenity's information (Admin only)
        """
        # ADMIN CHECK
        claims = get_jwt()
        if not claims.get('is_admin'):
            api.abort(403, "Admin privileges required to update amenities.")

        if not amenity_id or not isinstance(amenity_id, str) or len(amenity_id.strip()) == 0:
            api.abort(400, "Amenity ID cannot be empty or invalid.")
        
        data = api.payload
        name = data.get('name')
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            api.abort(400, "Amenity name cannot be empty or invalid.")
        
        # Check if amenity exists
        if not facade.get_amenity(amenity_id):
            api.abort(404, f"Amenity with ID '{amenity_id}' not found")

        # Check for name duplication
        existing_amenity_with_same_name = facade.get_amenity_by_name(name)
        
        if existing_amenity_with_same_name:
            existing_id = existing_amenity_with_same_name['id'] if isinstance(existing_amenity_with_same_name, dict) else existing_amenity_with_same_name.id
            if existing_id != amenity_id:
                api.abort(409, f"Another amenity with name '{name}' already exists.")
            
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            return updated_amenity
        except ValueError as e:
            api.abort(400, str(e))
