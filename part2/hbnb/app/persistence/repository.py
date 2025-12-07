#!/usr/bin/python3
"""
Repository pattern implementation
"""
from abc import ABC, abstractmethod
from app import db
from sqlalchemy.exc import IntegrityError
from app.models.user import User

class Repository(ABC):
    """
    Abstract Base Class for Repositories
    """
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """
    In-memory storage for development/testing without DB
    """
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)


class SQLAlchemyRepository(Repository):
    """
    Database storage using SQLAlchemy.
    This works as a generic repository for any model.
    """
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback() 
            raise ValueError(f"Integrity Error: {str(e.orig)}")
        except Exception as e:
            db.session.rollback()
            raise e

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                # Prevent updating ID or restricted fields
                if hasattr(obj, key) and key != 'id':
                    setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()


class UserRepository(SQLAlchemyRepository):
    """
    Specific repository for Users.
    Inherits generic logic from SQLAlchemyRepository but sets the User model
    and adds user-specific queries.
    """
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        """
        Specific method to find a user by email
        """
        return self.get_by_attribute('email', email)
