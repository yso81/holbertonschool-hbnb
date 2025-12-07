#!/usr/bin/python3
from app.persistence import user_repository
from app.models.user import User

class UserService:
    def create_user(self, data):
        # Create the user object
        user = User(**data)
        
        # Use the repository to add it to the DB
        user_repository.add(user)
        return user

    def get_user(self, user_id):
        # Use the repository to fetch the user
        return user_repository.get(user_id)
        
    def get_user_by_email(self, email):
        return user_repository.get_by_attribute('email', email)