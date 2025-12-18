#!/usr/bin/python3
"""
Facade Pattern implementation.
This layer acts as an interface between the API and the Persistence layer.
"""
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence import (
    user_repository,
    place_repository,
    review_repository,
    amenity_repository
)

class HBnBFacade:
    """
    The Facade class handles business logic and coordinates
    storage operations using the repositories.
    """
    
    def __init__(self):
        """
        The repositories are imported from app.persistence, 
        where they are already instantiated based on configuration.
        """
        self.user_repo = user_repository
        self.place_repo = place_repository
        self.review_repo = review_repository
        self.amenity_repo = amenity_repository

    # USER METHODS

    def create_user(self, user_data):
        """Creates a new user"""
        if not user_data.get('email') or not user_data.get('password'):
            raise ValueError("Email and password are required")

        if self.user_repo.get_by_email(user_data['email']):
            raise ValueError("Email already registered")
        
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get user by Email"""
        return self.user_repo.get_by_email(email)
    
    def find_users_by_name(self, first_name):
        """
        Searches users by first name (case-insensitive).
        """
        all_users = self.user_repo.get_all()
        results = []
        for user in all_users:
            if user.first_name and user.first_name.lower() == first_name.lower():
                results.append(user)
        return results

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """Update user data"""
        return self.user_repo.update(user_id, data)

    # AMENITY METHODS

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        name = amenity_data.get("name")
        if not name or not name.strip():
            raise ValueError("Name is required")

        if hasattr(self.amenity_repo, 'get_by_name'):
            existing = self.amenity_repo.get_by_name(name.strip())
        else:
            existing = self.amenity_repo.get_by_attribute("name", name.strip())

        if existing:
             raise ValueError(f"Amenity '{name.strip()}' already exists.")

        new_amenity = Amenity(name=name.strip())
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """Get amenity by name"""
        if hasattr(self.amenity_repo, 'get_by_name'):
            return self.amenity_repo.get_by_name(name)
        return self.amenity_repo.get_by_attribute("name", name)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity"""
        return self.amenity_repo.update(amenity_id, amenity_data)

    # PLACE METHODS

    def create_place(self, place_data):
        """Create a new place"""
        user_id = place_data.get('user_id')
        if not user_id or not self.user_repo.get(user_id):
            raise ValueError(f"Owner with ID '{user_id}' not found.")
        
        if 'price' in place_data:
             place_data['price_by_night'] = place_data.pop('price')

        amenity_ids = place_data.pop('amenity_ids', [])
        
        try:
            if 'price_by_night' in place_data:
                place_data['price_by_night'] = float(place_data['price_by_night'])
            place_data['latitude'] = float(place_data.get('latitude', 0.0))
            place_data['longitude'] = float(place_data.get('longitude', 0.0))
        except (ValueError, TypeError):
             raise ValueError("Price, latitude, and longitude must be valid numbers.")

        new_place = Place(**place_data)
        
        if amenity_ids:
            for am_id in amenity_ids:
                amenity = self.amenity_repo.get(am_id)
                if amenity:
                    new_place.amenities.append(amenity)

        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, update_data):
        """Update place"""
        if 'price' in update_data:
            update_data['price_by_night'] = update_data.pop('price')
            
        return self.place_repo.update(place_id, update_data)
    
    def delete_place(self, place_id):
        """Delete place"""
        return self.place_repo.delete(place_id)

    # REVIEW METHODS

    def create_review(self, review_data):
        """Create a new review"""
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if not self.user_repo.get(user_id):
            raise ValueError("User not found")
            
        if not self.place_repo.get(place_id):
            raise ValueError("Place not found")

        # Check for duplicate review
        if hasattr(self.review_repo, 'get_by_place'):
            place_reviews = self.review_repo.get_by_place(place_id)
            for r in place_reviews:
                if str(r.user_id) == str(user_id):
                     raise ValueError("User has already reviewed this place")
        else:
            all_reviews = self.review_repo.get_all()
            for r in all_reviews:
                if str(r.user_id) == str(user_id) and str(r.place_id) == str(place_id):
                    raise ValueError("User has already reviewed this place")

        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_reviews_for_place(self, place_id):
        """
        Get reviews for a specific place.
        Uses specialized repo method if available, else filters all.
        """
        if hasattr(self.review_repo, 'get_by_place'):
             return self.review_repo.get_by_place(place_id)
        
        all_reviews = self.review_repo.get_all()
        return [r for r in all_reviews if str(r.place_id) == str(place_id)]

    def get_reviews_by_place(self, place_id):
        """
        Get all reviews for a specific place.
        Alias for get_reviews_for_place to ensure API compatibility.
        """
        return self.get_reviews_for_place(place_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def update_review(self, review_id, update_data):
        """Update review"""
        return self.review_repo.update(review_id, update_data)

    def delete_review(self, review_id):
        """Delete review"""
        return self.review_repo.delete(review_id)
