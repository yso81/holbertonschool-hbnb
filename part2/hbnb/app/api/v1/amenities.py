from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

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
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_create_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = request.get_json()
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
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity with ID '{amenity_id}' not found")
        return amenity

    @api.expect(amenity_create_model, validate=True)
    @api.marshal_with(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = request.get_json()
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            if not updated_amenity:
                api.abort(404, f"Amenity with ID '{amenity_id}' not found")
            return updated_amenity
        except ValueError as e:
            api.abort(400, str(e))
