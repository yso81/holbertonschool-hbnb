#!/usr/bin/python3
from app import create_app
from app.services import facade

app = create_app()

with app.app_context():
    # 1. Check if admin exists
    existing = facade.get_user_by_email("admin@hbnb.io")
    
    if existing:
        # If using InMemory, direct assignment works
        existing.is_admin = True
        print(f"Updated existing user {existing.first_name} to Admin.")
    else:
        # 2. Create new user
        user_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@hbnb.io",
            "password": "adminpassword"
        }
        # Create user (returns dict)
        new_user_dict = facade.create_user(user_data)
        
        # Get object to modify attribute
        user_obj = facade.get_user(new_user_dict['id'])
        user_obj.is_admin = True
        
        print(f"Admin User created with ID: {new_user_dict['id']}")
