#!/usr/bin/python3
import os
from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        """
        Initializes repositories based on the environment configuration.
        """
        # Check environment variable to determine storage type
        if os.getenv('USE_DATABASE') == 'True':
            self.user_repo = SQLAlchemyRepository(User)
            self.place_repo = SQLAlchemyRepository(Place)
            self.review_repo = SQLAlchemyRepository(Review)
            self.amenity_repo = SQLAlchemyRepository(Amenity)
        else:
            self.user_repo = InMemoryRepository()
            self.place_repo = InMemoryRepository()
            self.review_repo = InMemoryRepository()
            self.amenity_repo = InMemoryRepository()

    # USER METHODS

    def create_user(self, user_data):
        """Creates a new user"""
        if not user_data.get('email') or not user_data.get('password'):
            raise ValueError("Email and password are required")

        if self.user_repo.get_by_attribute('email', user_data['email']):
            raise ValueError("Email already registered")
        
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def find_users_by_name(self, first_name):
        """Searches users by first name (case-insensitive)"""
        all_users = self.user_repo.get_all()
        results = []
        for user in all_users:
            if user.first_name and user.first_name.lower() == first_name.lower():
                results.append(user)
        return results

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    # AMENITY METHODS

    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")
        if not name or not name.strip():
            raise ValueError("Name is required")

        if self.amenity_repo.get_by_attribute("name", name.strip()):
            raise ValueError(f"Amenity '{name.strip()}' already exists.")

        new_amenity = Amenity(name=name.strip())
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute("name", name)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    # PLACE METHODS

    def create_place(self, place_data):
        user_id = place_data.get('user_id')
        if not user_id or not self.user_repo.get(user_id):
            raise ValueError(f"Owner with ID '{user_id}' not found.")

        amenity_ids = place_data.pop('amenity_ids', [])
        
        try:
            place_data['price'] = float(place_data['price'])
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
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, update_data):
        return self.place_repo.update(place_id, update_data)
    
    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # REVIEW METHODS

    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if not self.user_repo.get(user_id):
            raise ValueError("User not found")
            
        if not self.place_repo.get(place_id):
            raise ValueError("Place not found")

        all_reviews = self.review_repo.get_all()
        for r in all_reviews:
            if str(r.user_id) == str(user_id) and str(r.place_id) == str(place_id):
                raise ValueError("User has already reviewed this place")

        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_reviews_for_place(self, place_id):
        all_reviews = self.review_repo.get_all()
        return [r for r in all_reviews if str(r.place_id) == str(place_id)]

    def update_review(self, review_id, update_data):
        return self.review_repo.update(review_id, update_data)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
        return True
