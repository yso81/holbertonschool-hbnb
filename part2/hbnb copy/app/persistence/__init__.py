#!/usr/bin/python3
"""
Initializes the persistence package.
"""
from app.persistence.repository import SQLAlchemyRepository, UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

user_repository = UserRepository()
place_repository = PlaceRepository()
review_repository = ReviewRepository()
amenity_repository = AmenityRepository()
