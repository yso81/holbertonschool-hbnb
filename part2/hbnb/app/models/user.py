#!/usr/bin/python3
"""
Module for the User class.
"""
from .base_model import BaseModel


class User(BaseModel):
    """
    User class that inherits from BaseModel
    Defines attributes for a user
    """
    first_name = ""
    last_name = ""
    email = ""
    password = ""
    is_admin = False

    def __init__(self, *args, **kwargs):
        """
        Initializes a new User
        """
        super().__init__()

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def to_dict(self):
        """
        Returns a dictionary representation of the User instance.
        """
        obj_dict = super().to_dict()

        obj_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        })
        return obj_dict
