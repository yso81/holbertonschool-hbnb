#!/usr/bin/python3
"""
Initializes the models package.

This file makes the models directory a Python package and imports all the
model classes to make them easily accessible from other modules
"""
from .base_model import BaseModel
from .user import User
from .place import Place
from .amenity import Amenity
from .review import Review
