#!/usr/bin/python3
import sys
import os
import re
from flask_restx import Namespace, Resource, fields, reqparse, abort

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)
from app.services import facade


api = Namespace('users', description='User operations')

email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Define the user model for input validation and documentation
user_input_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_details_model = api.inherit('UserDetails', user_input_model, {
    'id': fields.String(readonly=True, description='The user unique identifier')
})

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, help='Filter users by first name')

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_input_model)
    def get(self):
        """List all users"""
        args = parser.parse_args()
        first_name_filter = args.get('first_name')

        if first_name_filter:
            return facade.find_users_by_name(first_name_filter)
        else:
            return facade.get_all_users()

    @api.doc('create_user')
    @api.expect(user_input_model)
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

        if not email:
            return {"error": "Invalid input data"}, 400
        if not email_regex.match(email):
            return {"error": "Invalid input data"}, 400
        if not first_name or not last_name:
            return {"error": "Invalid input data"}, 400

        if facade.get_user_by_email(user_data['email']):
            api.abort(409, f"User with email '{user_data['email']}' already exists")

        new_user_dict = facade.create_user(user_data)
        return new_user_dict, 201

@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user_details')
    @api.marshal_with(user_details_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID
        """
        user_dict = facade.get_user(user_id)
        if not user_dict:
            return {'error': 'User not found'}, 404
        return user_dict, 200

    @api.doc('update_user')
    @api.expect(user_input_model)
    @api.marshal_with(user_details_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        update a user details
        """
        user_data = api.payload

        email = user_data.get('email')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')

        if not email:
            return {"error": "Invalid input data"}, 400
        if not email_regex.match(email):
            return {"error": "Invalid input data"}, 400
        if not first_name or not last_name:
            return {"error": "Invalid input data"}, 400

        updated_user_dict = facade.update_user(user_id, user_data)

        if not updated_user_dict:
            api.abort(404, f"User {user_id} not found")
            
        return updated_user_dict, 200
