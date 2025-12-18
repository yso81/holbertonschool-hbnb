#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.extensions import jwt, bcrypt
from config import config
from flask_cors import CORS

# Initialize SQLAlchemy instance globally
db = SQLAlchemy()

def create_app(config_name="config.DevelopmentConfig"):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 1. Load Configuration
    app.config.from_object(config_name)

    # 2. Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # 3. Configure Swagger UI to support JWT
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**"
        }
    }

    api = Api(
        app, 
        version='1.0', 
        title='HBnB API', 
        description='HBnB Application API', 
        doc='/api/v1/doc/',
        authorizations=authorizations,
        security='Bearer Auth'
    )

    # 4. Register Namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1 import blueprint as api_v1

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    app.register_blueprint(api_v1)

    return app
