#!/usr/bin/python3
"""
Module for the User class
"""
from app import db
from app.extensions import bcrypt
from app.models.base_model import BaseModel

class User(BaseModel):
    """
    User class that inherits from BaseModel
    """
    __tablename__ = 'users'

    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new User
        Calls the BaseModel init and hashes the password if provided
        """
        raw_password = kwargs.pop('password', None)
        
        super().__init__(*args, **kwargs)
        
        if raw_password:
            self.hash_password(raw_password)

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

        if "password" in obj_dict:
            del obj_dict["password"]

        return obj_dict
