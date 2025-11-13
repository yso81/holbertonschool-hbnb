#!/usr/bin/python3
import sys
import os
from flask_restx import Namespace, Resource, fields
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)
from app.services import facade


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_input_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_details_model = api.inherit('UserDetails', user_input_model, {
    'id': fields.String(readonly=True, description='The user unique identifier')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_input_model)
    def get(self):
        """List all users"""
        users = facade.get_all_users() 
        return users

    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_details_model, code=201)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id, 
            'first_name': new_user.first_name, 
            'last_name': new_user.last_name, 
            'email': new_user.email
            }, 201


@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.marshal_with(user_details_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email
            }, 200

    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_details_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        update a user details
        """
        user_data = api.payload

        updated_user = facade.update_user(user_id, user_data)

        if not updated_user:
            api.abort(404, f"User {user_id} not found")
            
        return updated_user, 200
