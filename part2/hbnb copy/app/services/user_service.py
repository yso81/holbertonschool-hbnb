#!/usr/bin/python3
"""
Service layer for User business logic.
"""
from typing import List, Optional
from app.models.user import User
from app.persistence import user_repository

class UserService:
    """
    Handles business logic for Users.
    """

    def create_user(self, data: dict) -> User:
        """
        Creates a new user.
        Validates email uniqueness and required fields.
        """
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise ValueError("Email and password are required.")

        if user_repository.get_by_email(email):
            raise ValueError("A user with this email already exists.")

        # Create User
        user = User(**data)
        
        # Persistence
        user_repository.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """
        Retrieves a user by ID.
        """
        return user_repository.get(user_id)
        
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by email.
        """
        return user_repository.get_by_email(email)

    def get_all_users(self) -> List[User]:
        """
        Retrieves all users.
        """
        return user_repository.get_all()

    def update_user(self, user_id: str, data: dict) -> Optional[User]:
        """
        Updates user details.
        """
        if 'id' in data:
            del data['id']
        if 'email' in data:
            existing = user_repository.get_by_email(data['email'])
            if existing and existing.id != user_id:
                raise ValueError("Email is already in use by another user.")

        return user_repository.update(user_id, data)

    def delete_user(self, user_id: str) -> bool:
        """
        Deletes a user.
        """
        return user_repository.delete(user_id)