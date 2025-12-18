#!/usr/bin/python3
import sys
import os
import re
from flask_restx import Namespace, Resource, fields, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)
from app.services import facade

api = Namespace('users', description='User operations')

email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
UUID_REGEX = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')

user_base_model = api.model('UserBase', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_create_model = api.inherit('UserCreate', user_base_model, {
    'password': fields.String(required=True, description='Password for the user account'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

user_details_model = api.inherit('UserResponse', user_base_model, {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'is_admin': fields.Boolean(readonly=True, description='Admin status'),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Update timestamp'),
})

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, help='Filter users by first name')

@api.route('/')
class UserList(Resource):
    @api.doc('list_users', security='Bearer Auth')
    @api.marshal_list_with(user_details_model)
    @jwt_required()
    def get(self):
        """List all users"""
        args = parser.parse_args()
        first_name_filter = args.get('first_name')

        if first_name_filter:
            if not isinstance(first_name_filter, str) or len(first_name_filter.strip()) == 0:
                api.abort(400, "Invalid first name filter provided.")

            return facade.find_users_by_name(first_name_filter)
        else:
            return facade.get_all_users()

    @api.doc('create_user') 
    @api.expect(user_create_model)
    @api.marshal_with(user_details_model, code=201)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""

        user_data = api.payload

        email = user_data.get('email')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        password = user_data.get('password')

        if not email or not isinstance(email, str) or len(email.strip()) == 0:
            api.abort(400, "Invalid or missing 'email'.")
        if not email_regex.match(email):
            api.abort(400, "Invalid email format.")

        if not first_name or not isinstance(first_name, str) or len(first_name.strip()) == 0:
            api.abort(400, "Invalid or missing 'first_name'. Must be a non-empty string")
        
        if not last_name or not isinstance(last_name, str) or len(last_name.strip()) == 0:
            api.abort(400, "Invalid or missing 'last_name'. Must be a non-empty string")

        if not password or not isinstance(password, str) or len(password.strip()) == 0:
            api.abort(400, "Invalid or missing 'password'. Must be a non-empty string")

        if facade.get_user_by_email(user_data['email']):
            api.abort(409, f"User with email '{user_data['email']}' already exists")

        try:
            new_user = facade.create_user(user_data)
            return new_user, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user_details', security='Bearer Auth')
    @api.marshal_with(user_details_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self, user_id):
        """
        Get user details by ID
        """
        if not UUID_REGEX.match(user_id):
            api.abort(400, "Invalid user ID format. Must be a UUID.")

        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with ID '{user_id}' not found")
        return user

    @api.doc('update_user', security='Bearer Auth')
    @api.expect(user_base_model)
    @api.marshal_with(user_details_model)
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """
        update a user details (Owner or Admin)
        """
        if not UUID_REGEX.match(user_id):
            api.abort(400, "Invalid user ID format. Must be a UUID.")

        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if current_user_id != user_id and not is_admin:
            api.abort(403, "Unauthorized action")

        user_data = api.payload

        existing_user = facade.get_user(user_id)
        if not existing_user:
            api.abort(404, f"User {user_id} not found")

        email = user_data.get('email')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')

        if not email or not isinstance(email, str) or len(email.strip()) == 0:
            api.abort(400, "Invalid or missing 'email'.")
        if not email_regex.match(email):
            api.abort(400, "Invalid email format.")

        if not first_name or not isinstance(first_name, str) or len(first_name.strip()) == 0:
            api.abort(400, "Invalid or missing 'first_name'. Must be a non-empty string")
        
        if not last_name or not isinstance(last_name, str) or len(last_name.strip()) == 0:
            api.abort(400, "Invalid or missing 'last_name'. Must be a non-empty string")

        user_with_email = facade.get_user_by_email(email)
        if user_with_email and user_with_email.id != user_id:
            api.abort(400, f"Email '{email}' is already in use by another account.")

        updated_user = facade.update_user(user_id, user_data)

        if not updated_user:
            api.abort(404, f"User {user_id} not found")
            
        return updated_user, 200
