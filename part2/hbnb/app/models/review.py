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
    def __init__(self, *args, **kwargs):
        #Initializes a new Review
        super().__init__(*args, **kwargs)
        self.place_id = ""
        self.user_id = ""
        self.text = ""
        self.place = None
        self.user = None
