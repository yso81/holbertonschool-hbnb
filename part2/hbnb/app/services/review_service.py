#!/usr/bin/python3
"""
This module defines the ReviewService class.
"""
from typing import List, Optional, Dict, Any
from app.models.review import Review
from app.persistence import review_repository, user_repository, place_repository

class ReviewService:
    """
    The ReviewService class handles the business logic for reviews.
    """

    def create_review(self, review_data: Dict[str, Any]) -> Review:
        """
        Creates a new review.
        Validates existence of user/place, checks for duplicates, and validates rating.
        """
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')
        text = review_data.get('text')

        if not user_id or not place_id or text is None:
            raise ValueError("User ID, Place ID, and Text are required.")

        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer between 1 and 5.")
        
        if not user_repository.get(user_id):
            raise ValueError(f"User with ID {user_id} not found.")
        
        if not place_repository.get(place_id):
            raise ValueError(f"Place with ID {place_id} not found.")

        existing_reviews = review_repository.get_by_place(place_id)
        for review in existing_reviews:
            if review.user_id == user_id:
                raise ValueError("User has already reviewed this place.")

        new_review = Review(**review_data)
        review_repository.add(new_review)
        return new_review

    def get_review(self, review_id: str) -> Optional[Review]:
        """
        Retrieves a review by ID.
        """
        return review_repository.get(review_id)

    def get_all_reviews(self) -> List[Review]:
        """
        Retrieves all reviews.
        """
        return review_repository.get_all()

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        """
        Retrieves all reviews for a specific place.
        """
        return review_repository.get_by_place(place_id)

    def update_review(self, review_id: str, review_data: Dict[str, Any]) -> Optional[Review]:
        """
        Updates a review's details (text or rating).
        """
        if 'user_id' in review_data or 'place_id' in review_data:
            raise ValueError("Cannot change the User or Place associated with a review.")
        
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not (1 <= rating <= 5):
                    raise ValueError
                review_data['rating'] = rating
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5.")

        return review_repository.update(review_id, review_data)

    def delete_review(self, review_id: str) -> bool:
        """
        Deletes a review.
        """
        return review_repository.delete(review_id)
