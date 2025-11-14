#!/usr/bin/python3
"""
Initializes the Blueprint for API version 1.
"""
from flask import Blueprint
from flask_restx import Api
from .amenities import api as amenities_ns
from .users import api as users_ns

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    blueprint,
    title='HBnB API',
    version='1.0',
    prefix='/v1'
)

api.add_namespace(amenities_ns)
api.add_namespace(users_ns)
