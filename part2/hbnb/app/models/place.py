#!/usr/bin/python3
"""
Module for the Place class
"""
from .base_model import BaseModel


class Place(BaseModel):
    """
    Represents a place available for booking.

    Attributes:
        city_id (str): The ID of the city where the place is located.
        user_id (str): The ID of the user who owns the place.
        name (str): The name of the place.
        description (str): A description of the place.
        number_rooms (int): The number of rooms in the place.
        number_bathrooms (int): The number of bathrooms in the place.
        max_guest (int): The maximum number of guests the place can accommodate.
        price_by_night (int): The price per night for the place.
        latitude (float): The latitude of the place's location.
        longitude (float): The longitude of the place's location.
        owner (User): The User object who owns the place.
        reviews (list): A list of Review instances for the place.
        amenities (list): A list of Amenity instances for the place.
    """
    
    def __init__(self, *args, **kwargs):
        #Initializes a new Place
        super().__init__(*args, **kwargs)
        self.city_id = ""
        self.user_id = ""
        self.name = ""
        self.description = ""
        self.number_rooms = 0
        self.number_bathrooms = 0
        self.max_guest = 0
        self.price_by_night = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.owner = None
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        #Add a review to the place
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        #Add an amenity to the place
        if amenity not in self.amenities:
            self.amenities.append(amenity)
