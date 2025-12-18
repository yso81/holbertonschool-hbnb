#!/usr/bin/python3
"""
Module for the Review class
"""
from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    """
    Represents a review of a place
    """
    __tablename__ = 'reviews'

    # Content
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, default=0, nullable=False)

    # Foreign Keys
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    
    user = db.relationship('User', backref='reviews', lazy=True)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new Review
        """
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """
        Returns a dictionary representation of the Review instance
        """
        obj_dict = super().to_dict()
        obj_dict.update({
            "place_id": self.place_id,
            "user_id": self.user_id,
            "text": self.text,
            "rating": self.rating
        })
        return obj_dict