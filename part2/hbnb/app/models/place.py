#!/usr/bin/python3
"""
Module for the Place class
"""
from app import db
from app.models.base_model import BaseModel

# Table for the Many-to-Many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """
    Represents a place available for booking.
    """
    __tablename__ = 'places'

    # Foreign Keys
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Place Attributes
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    number_rooms = db.Column(db.Integer, default=0, nullable=False)
    number_bathrooms = db.Column(db.Integer, default=0, nullable=False)
    max_guest = db.Column(db.Integer, default=0, nullable=False)
    price_by_night = db.Column(db.Integer, default=0, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Cascade delete
    reviews = db.relationship('Review', backref='place', cascade='all, delete-orphan', lazy=True)
    
    # Many-to-Many relationship with Amenity
    amenities = db.relationship('Amenity', secondary=place_amenity, viewonly=False, backref='places')

    def __init__(self, *args, **kwargs):
        """
        Initializes a new Place
        """
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """
        Returns a dictionary representation of the Place instance
        """
        obj_dict = super().to_dict()
        obj_dict.update({
            "city_id": self.city_id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "number_rooms": self.number_rooms,
            "number_bathrooms": self.number_bathrooms,
            "max_guest": self.max_guest,
            "price_by_night": self.price_by_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
        })
        return obj_dict


    def add_review(self, review):
        """
        Add a review to the place.
        With SQLAlchemy, we can simply append to the relationship list.
        """
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to the place.
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)