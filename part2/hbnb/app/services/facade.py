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
        return user.to_dict()

    def get_user(self, user_id):
        """
        Retrieves a user by their id
        """
        user = self.user_repo.get(user_id)
        return user.to_dict() if user else None

    def get_all_users(self):
        """
        Retrieves all users from the repository.
        """
        return [user.to_dict() for user in self.user_repo.get_all()]
        
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

        user_obj = self.user_repo.get(user_id)
        if not user_obj:
            return None

        for key, value in data.items():
            if hasattr(user_obj, key):
                setattr(user_obj, key, value)
        
        user_obj.save()
        self.user_repo.save(user_obj)
        return user_obj.to_dict()
    
    def find_users_by_name(self, first_name):
        """
        Finds all users with a given first name.
        This method searches for users where the 'first_name' attribute matches.
        
        Args:
            first_name (str): The first name to search for.

        Returns:
            list: A list of user objects that match the first name.
                  Returns an empty list if no users are found.
        """
        matching_users = self.user_repo.get_by_attribute('first_name', first_name)
        
        return matching_users

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

    def create_place(self, place_data):
        """
        Creates a new place after validating related entities and data.
        """
        if not self.user_repo.get(place_data['user_id']):
            raise ValueError(f"Owner with ID '{place_data['user_id']}' not found.")
    
        if 'amenity_ids' in place_data:
            for amenity_id in place_data['amenity_ids']:
                if not self.amenity_repo.get(amenity_id):
                    raise ValueError(f"Amenity with ID '{amenity_id}' not found.")
    
        if not (0 <= float(place_data['price'])):
            raise ValueError("Price must be a non-negative number.")
        if not (-90 <= float(place_data['latitude']) <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= float(place_data['longitude']) <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        new_place = Place(**place_data)
        self.place_repo.add(new_user)
        return new_place

    def get_place(self, place_id):
        """Retrieves a single place by its ID."""
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """Retrieves all places from the repository."""
        return self.place_repo.get_all()

    def update_place(self, place_id, update_data):
        """
        Updates an existing place's information.
        """
        place_to_update = self.get_place(place_id)
        if not place_to_update:
            return None

        if 'price' in update_data and not (0 <= float(update_data['price'])):
            raise ValueError("Price must be a non-negative number.")
        
        for key, value in update_data.items():
            setattr(place_to_update, key, value)
        
        place_to_update.updated_at = datetime.now()

        self.place_repo.save(place_to_update)
        return place_to_update

    def create_review(self, review_data):
        """
        Creates a new review after validating entities
        
        Args:
            review_data (dict): Data for the new review. Must include
            'user_id', 'place_id', 'rating', and 'comment'
        
        Returns:
            Review: The newly created review object
        
        Raises:
            ValueError: If user or place is not found, or rating is invalid
        """
        if not self.user_repo.get(review_data['user_id']):
            raise ValueError(f"User with ID '{review_data['user_id']}' not found.")
        if not self.place_repo.get(review_data['place_id']):
            raise ValueError(f"Place with ID '{review_data['place_id']}' not found.")
        
        rating = review_data.get('rating')
        if not (1 <= int(rating) <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")

        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        """Retrieves a single review by its ID."""
        return self.review_repo.get(review_id)
    
    def get_reviews_for_place(self, place_id):
        """Retrieves all reviews for a specific place."""
        if not self.place_repo.get(place_id):
            raise ValueError(f"Place with ID '{place_id}' not found.")
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, update_data):
        """
        Updates an existing review
        
        Args:
            review_id (str): The ID of the review to update
            update_data (dict): A dictionary with the new 'rating' or 'comment'
            
        Returns:
            Review: The updated review object, or None if not found
        
        Raises:
            ValueError: If the rating is invalid
        """
        review_to_update = self.get_review(review_id)
        if not review_to_update:
            return None

        if 'rating' in update_data:
            rating = update_data['rating']
            if not (1 <= int(rating) <= 5):
                raise ValueError("Rating must be an integer between 1 and 5.")
            review_to_update.rating = rating

        if 'comment' in update_data:
            review_to_update.comment = update_data['comment']
        
        review_to_update.updated_at = datetime.now()
        self.review_repo.save(review_to_update)
        return review_to_update

    def delete_review(self, review_id):
        """
        Deletes a review by its ID.
        
        Args:
            review_id (str): The ID of the review to delete.
            
        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        review_to_delete = self.get_review(review_id)
        if not review_to_delete:
            return False
            
        self.review_repo.delete(review_id)
        return True
