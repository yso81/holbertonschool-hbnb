#!/usr/bin/python3
"""
This module defines the PlaceService class
"""
from typing import List, Optional, Dict, Any
from app.models.place import Place
from app.persistence import place_repository, user_repository

class PlaceService:
    """
    The PlaceService class handles the business logic for places.
    It orchestrates validation and persistence.
    """

    def create_place(self, place_data: Dict[str, Any]) -> Place:
        """
        Creates a new place after validating data.
        """
        user_id = place_data.get('user_id')
        if not user_id:
            raise ValueError("User ID is required.")
        
        user = user_repository.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")

        if 'price' in place_data:
            place_data['price_by_night'] = place_data.pop('price')

        try:
            if 'price_by_night' in place_data:
                place_data['price_by_night'] = float(place_data['price_by_night'])
            if 'latitude' in place_data:
                place_data['latitude'] = float(place_data['latitude'])
            if 'longitude' in place_data:
                place_data['longitude'] = float(place_data['longitude'])
            if 'max_guest' in place_data:
                place_data['max_guest'] = int(place_data['max_guest'])
        except (ValueError, TypeError):
            raise ValueError("Price, latitude, longitude, and max_guest must be valid numbers.")

        amenity_ids = place_data.pop('amenity_ids', [])
        
        place = Place(**place_data)
        
        place_repository.add(place)
        return place

    def get_place(self, place_id: str) -> Optional[Place]:
        """
        Retrieves a place by its ID.
        """
        return place_repository.get(place_id)

    def get_all_places(self) -> List[Place]:
        """
        Retrieves all places.
        """
        return place_repository.get_all()

    def get_places_by_owner(self, user_id: str) -> List[Place]:
        """
        Retrieves all places owned by a specific user.
        """
        return place_repository.get_by_owner(user_id)

    def update_place(self, place_id: str, place_data: Dict[str, Any]) -> Optional[Place]:
        """
        Updates a place's details.
        """
        if 'user_id' in place_data:
            raise ValueError("Cannot transfer ownership via update_place.")
        if 'id' in place_data:
            del place_data['id']

        if 'price' in place_data:
            place_data['price_by_night'] = place_data.pop('price')

        return place_repository.update(place_id, place_data)

    def delete_place(self, place_id: str) -> bool:
        """
        Deletes a place.
        """
        return place_repository.delete(place_id)
