#!/usr/bin/python3
"""
Module for the Amenity class
"""
from app import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with a place.
    """
    __tablename__ = 'amenities'

    # Columns
    name = db.Column(db.String(128), nullable=False, unique=False)
    

    def __init__(self, *args, **kwargs):
        """
        Initializes a new Amenity
        """
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """
        Returns a dictionary representation of the Amenity instance
        """
        obj_dict = super().to_dict()
        obj_dict.update({
            "name": self.name
        })
        return obj_dict
