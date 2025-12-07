#!/usr/bin/python3
"""
Initializes the persistence package.
"""
from app.persistence.repository import SQLAlchemyRepository, UserRepository
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

user_repository = UserRepository()

# Initialize repositories with their specific models
place_repository = SQLAlchemyRepository(Place)
review_repository = SQLAlchemyRepository(Review)
amenity_repository = SQLAlchemyRepository(Amenity)