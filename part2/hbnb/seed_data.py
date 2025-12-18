from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.services import facade
import sys

app = create_app()

def seed_database():
    with app.app_context():
        print("Clearing old data...")
        db.drop_all() 
        db.create_all() 
        print("Database clean.")

        print("Seeding Database...")

        # --- 1. Create Users ---
        user1 = User(first_name="Alice", last_name="Wonder", email="alice@test.com", password="password123")
        user2 = User(first_name="Bob", last_name="Builder", email="bob@test.com", password="password123")
        user3 = User(first_name="Charlie", last_name="Chocolate", email="charlie@test.com", password="password123")

        db.session.add_all([user1, user2, user3])
        db.session.commit()
        print("Created 3 Users")

        # --- 2. Create Amenities ---
        wifi = Amenity(name="WiFi")
        pool = Amenity(name="Swimming Pool")
        ac = Amenity(name="Air Conditioning")
        parking = Amenity(name="Free Parking")

        db.session.add_all([wifi, pool, ac, parking])
        db.session.commit()
        print("Created 4 Amenities")

        # --- 3. Create Places ---
        
        place1 = Place(
            name="Cozy Mountain Cottage",
            description="A lovely cottage in the hills with a fireplace and amazing views.",
            address="123 Alpine Road",
            city_name="PeaksVille",
            price_by_night=120,
            latitude=37.7749,
            longitude=-122.4194,
            user_id=user1.id,
            number_rooms=2,
            number_bathrooms=1,
            max_guest=4,
            amenities=[wifi, parking]
        )
        
        place2 = Place(
            name="Modern Downtown Loft",
            description="Stylish loft in the city center. Walking distance to everything.",
            address="456 Main St",
            city_name="Metropolis",
            price_by_night=50,
            latitude=40.7128,
            longitude=-74.0060,
            user_id=user2.id,
            number_rooms=1,
            number_bathrooms=1,
            max_guest=2,
            amenities=[wifi, ac]
        )

        place3 = Place(
            name="Luxury Beach Villa",
            description="Private villa right on the sand. Includes private pool and chef.",
            address="789 Ocean Blvd",
            city_name="Seaside",
            price_by_night=5,
            latitude=25.7617,
            longitude=-80.1918,
            user_id=user1.id,
            number_rooms=5,
            number_bathrooms=4,
            max_guest=10,
            amenities=[wifi, pool, ac, parking]
        )

        db.session.add_all([place1, place2, place3])
        db.session.commit()
        print("Created 3 Places with Locations and Amenities")

        # --- 4. Create Reviews ---
        review1 = Review(text="Absolutely loved this place!", rating=5, user_id=user2.id, place_id=place1.id)
        review2 = Review(text="Nice, but a bit cold.", rating=4, user_id=user3.id, place_id=place1.id)
        review3 = Review(text="Noisy location.", rating=3, user_id=user3.id, place_id=place2.id)

        db.session.add_all([review1, review2, review3])
        db.session.commit()

        print("Created 3 Reviews")
        print("Database populated successfully!")

if __name__ == "__main__":
    seed_database()
