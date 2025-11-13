#!/usr/bin/python3
"""
HBnBFacade class initializes and maintains references to the various services
and repositories required by the application
"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.services.user_service import UserService
from app.services.place_service import PlaceService
from app.services.review_service import ReviewService
from app.services.amenity_service import AmenityService


class HBnBFacade:
    def __init__(self):
        """
        Initializes all repositories
        """
        self.user_service = UserService()
        self.place_service = PlaceService()
        self.review_service = ReviewService()
        self.amenity_service = AmenityService()

        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        """
        Creates a new user and adds it to the repository
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieves a user by their id
        """
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """
        Retrieves all users from the repository.
        """
        return self.user_repo.get_all()
        
    def get_user_by_email(self, email):
        """
        retrieves a user by their email address
        """
        users = self.user_repo.get_by_attribute('email', email)
        if users:
            return users[0]
        return None

    def update_user(self, user_id, data):
        """
        Updates an existing user's information.

        Args:
            user_id (str): The ID of the user to update.
            data (dict): A dictionary containing the new data for the user.

        Returns:
            User: The updated user object, or None if the user was not found.
        """
        user_to_update = self.get_user(user_id)

        if not user_to_update:
            return None

        for key, value in data.items():
            setattr(user_to_update, key, value)

        repo.save(user_to_update)

        return user_to_update

    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
    pass

    def get_amenity(self, amenity_id):
    # Placeholder for logic to retrieve an amenity by ID
    pass

    def get_all_amenities(self):
    # Placeholder for logic to retrieve all amenities
    pass

    def update_amenity(self, amenity_id, amenity_data):
    # Placeholder for logic to update an amenity
    pass
