#!/usr/bin/python3
"""
HBnBFacade class initializes and maintains references to the various services
and repositories required by the application
"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services.user_service import UserService
from app.services.place_service import PlaceService
from app.services.review_service import ReviewService
from app.services.amenity_service import AmenityService
from uuid import UUID


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
        """
        Create a new amenity.

        :param amenity_data: A dictionary with 'name' of the amenity
        :return: The newly created Amenity object
        :raises ValueError: If the name is missing or invalid
        """
        name = amenity_data.get("name")
        if not name or not name.strip():
            raise ValueError("Name is required")

        new_amenity = Amenity(name=name.strip())
        self.amenity_repo.save(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        """
        Get an amenity by its ID.

        :param amenity_id: The unique ID of the amenity
        :return: The Amenity object or None if not found
        """
        try:
            UUID(amenity_id)  # Check if ID is valid
        except ValueError:
            return None  # If the ID is not valid

        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Get all amenities.

        :return: A list of all Amenity objects
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an amenity by ID.

        :param amenity_id: The ID of the amenity
        :param amenity_data: A dictionary with the new 'name'
        :return: The updated Amenity object, or None if not found
        :raises ValueError: If the name is invalid
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None  # Amenity not found

        name = amenity_data.get("name")
        if not name or not name.strip():
            raise ValueError("Name is required")

        amenity.name = name.strip()
        self.amenity_repo.save(amenity)
        return amenity
