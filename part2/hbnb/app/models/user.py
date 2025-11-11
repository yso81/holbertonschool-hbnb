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
                if hasattr(self, key):
                    setattr(self, key, value)
