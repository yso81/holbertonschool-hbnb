#!/usr/bin/python3
"""
Module for the Review class
"""
from .base_model import BaseModel


class Review(BaseModel):
    """
    Represents a review of a place

    Attributes:
        place_id (str): The ID of the place being reviewed
        user_id (str): The ID of the user who wrote the review
        text (str): The content of the review
        place (Place): The Place object being reviewed
        user (User): The User object who wrote the review
    """
    place_id = ""
    user_id = ""
    text = ""
    place = None
    user = None

    def __init__(self, *args, **kwargs):
        #Initializes a new Review
        super().__init__()
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
