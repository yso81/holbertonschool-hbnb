#!/usr/bin/python3
"""
Module for the User class.
"""
from app.models.base_model import BaseModel
from app.extensions import bcrypt


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
                if key == "password":
                    self.hash_password(value)
                else:
                    setattr(self, key, value)

    def hash_password(self, password):
        """
        Hashes the password before storing it
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verifies if the provided password matches the hashed password
        """
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """
        Returns a dictionary representation of the User instance
        """
        obj_dict = super().to_dict()

        obj_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        })

        # Ensure password is strictly removed from the output dictionary
        if "password" in obj_dict:
            del obj_dict["password"]

        return obj_dict
