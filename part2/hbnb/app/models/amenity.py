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
    def __init__(self, *args, **kwargs):
        #Initializes a new Amenity
        super().__init__(*args, **kwargs)
        self.name = ""
