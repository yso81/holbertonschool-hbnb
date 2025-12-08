#!/usr/bin/python3
"""
Repository pattern implementation
"""
from abc import ABC, abstractmethod
from typing import Type, List, Optional, Any, Dict
import uuid
from sqlalchemy.exc import IntegrityError
from app import db

# Import all models
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class Repository(ABC):
    """
    Abstract Base Class for Repositories
    """
    @abstractmethod
    def add(self, obj: Any) -> Any:
        pass

    @abstractmethod
    def get(self, obj_id: Any) -> Optional[Any]:
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def update(self, obj_id: Any, data: Dict[str, Any]) -> Optional[Any]:
        pass

    @abstractmethod
    def delete(self, obj_id: Any) -> bool:
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[Any]:
        pass


class SQLAlchemyRepository(Repository):
    """
    Database storage using SQLAlchemy.
    This provides generic CRUD for any model.
    """
    def __init__(self, model: Type[db.Model]):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        try:
            db.session.commit()
            db.session.refresh(obj)
            return obj
        except IntegrityError as e:
            db.session.rollback() 
            raise ValueError(f"Integrity Error: {str(e.orig)}")
        except Exception as e:
            db.session.rollback()
            raise e

    def get(self, obj_id):
        return db.session.get(self.model, obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key) and key != 'id':
                    setattr(obj, key, value)
            try:
                db.session.commit()
                db.session.refresh(obj)
                return obj
            except IntegrityError:
                db.session.rollback()
                raise ValueError("Update failed: Integrity Error")
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
                return True
            except Exception:
                db.session.rollback()
                return False
        return False

    def get_by_attribute(self, attr_name, attr_value):
        kwargs = {attr_name: attr_value}
        return self.model.query.filter_by(**kwargs).first()


# Specific Repositories

class UserRepository(SQLAlchemyRepository):
    """
    Repository for User entities.
    Inherits Create, Read, Update, Delete from SQLAlchemyRepository.
    """
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.get_by_attribute('email', email)


class PlaceRepository(SQLAlchemyRepository):
    """
    Repository for Place entities.
    Inherits Create, Read, Update, Delete from SQLAlchemyRepository.
    """
    def __init__(self):
        super().__init__(Place)

    def get_by_city(self, city_id: str) -> List[Place]:
        """Get all places in a specific city"""
        return self.model.query.filter_by(city_id=city_id).all()
    
    def get_by_owner(self, user_id: str) -> List[Place]:
        """Get all places owned by a specific user"""
        return self.model.query.filter_by(user_id=user_id).all()


class ReviewRepository(SQLAlchemyRepository):
    """
    Repository for Review entities.
    Inherits Create, Read, Update, Delete from SQLAlchemyRepository.
    """
    def __init__(self):
        super().__init__(Review)

    def get_by_place(self, place_id: str) -> List[Review]:
        """Get all reviews for a specific place"""
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_by_user(self, user_id: str) -> List[Review]:
        """Get all reviews written by a specific user"""
        return self.model.query.filter_by(user_id=user_id).all()


class AmenityRepository(SQLAlchemyRepository):
    """
    Repository for Amenity entities.
    Inherits Create, Read, Update, Delete from SQLAlchemyRepository.
    """
    def __init__(self):
        super().__init__(Amenity)

    def get_by_name(self, name: str) -> Optional[Amenity]:
        """Get amenity by name (useful to check duplicates)"""
        return self.get_by_attribute('name', name)
