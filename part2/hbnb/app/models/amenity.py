#!/usr/bin/python3
"""
Module for the Amenity class
"""
from .base_model import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with a place

    Attributes:
        name (str): The name of the amenity
    """
    name = ""

    def __init__(self, *args, **kwargs):
        #Initializes a new Amenity
        super().__init__()
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
