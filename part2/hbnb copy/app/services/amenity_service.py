#!/usr/bin/python3
"""
This module defines the AmenityService class
"""
from typing import List, Optional, Dict, Any
from app.models.amenity import Amenity
from app.persistence import amenity_repository

class AmenityService:
    """
    The AmenityService class handles the business logic for amenities
    """

    def create_amenity(self, amenity_data: Dict[str, Any]) -> Amenity:
        """
        Creates a new amenity
        Validates that the name is provided and ensures it is unique
        """
        name = amenity_data.get('name')

        if not name or not name.strip():
            raise ValueError("Amenity name is required.")
        
        name = name.strip()

        existing_amenity = amenity_repository.get_by_name(name)
        if existing_amenity:
            raise ValueError(f"Amenity '{name}' already exists.")

        amenity = Amenity(name=name)
        amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        """
        Retrieves an amenity by its ID.
        """
        return amenity_repository.get(amenity_id)

    def get_amenity_by_name(self, name: str) -> Optional[Amenity]:
        """
        Retrieves an amenity by its name.
        """
        return amenity_repository.get_by_name(name)

    def get_all_amenities(self) -> List[Amenity]:
        """
        Retrieves all available amenities.
        """
        return amenity_repository.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: Dict[str, Any]) -> Optional[Amenity]:
        """
        Updates an amenity's details.
        """
        if 'name' in amenity_data:
            new_name = amenity_data['name']
            if not new_name or not new_name.strip():
                raise ValueError("Amenity name cannot be empty.")
            
            existing = amenity_repository.get_by_name(new_name.strip())
            if existing and existing.id != amenity_id:
                raise ValueError(f"Amenity '{new_name}' already exists.")

        return amenity_repository.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id: str) -> bool:
        """
        Deletes an amenity.
        """
        return amenity_repository.delete(amenity_id)
