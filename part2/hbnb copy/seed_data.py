from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.services import facade

app = create_app()

def seed_database():
    with app.app_context():
        print("Clearing old data...")
        db.drop_all() 
        db.create_all() 
        print("Database clean.")

        print("Seeding Database...")

        user1 = User(first_name="Alice", last_name="Wonder", email="alice@test.com", password="password123")
        user2 = User(first_name="Bob", last_name="Builder", email="bob@test.com", password="password123")
        user3 = User(first_name="Charlie", last_name="Chocolate", email="charlie@test.com", password="password123")

        facade.user_repo.add(user1)
        facade.user_repo.add(user2)
        facade.user_repo.add(user3)
        print("Created 3 Users: Alice, Bob, Charlie")

        place1 = Place(
            title="Cozy Mountain Cottage",
            description="A lovely cottage in the hills with a fireplace and amazing views.",
            price=120.0,
            latitude=37.7749,
            longitude=-122.4194,
            owner_id=user1.id
        )
        
        place2 = Place(
            title="Modern Downtown Loft",
            description="Stylish loft in the city center. Walking distance to everything.",
            price=250.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=user2.id
        )

        place3 = Place(
            title="Luxury Beach Villa",
            description="Private villa right on the sand. Includes private pool and chef.",
            price=500.0,
            latitude=25.7617,
            longitude=-80.1918,
            owner_id=user1.id 
        )

        if hasattr(place1, 'amenities'): place1.amenities = ["Wifi", "Fireplace"]
        if hasattr(place2, 'amenities'): place2.amenities = ["AC", "Gym"]
        if hasattr(place3, 'amenities'): place3.amenities = ["Pool", "Beachfront", "Wifi"]

        facade.place_repo.add(place1)
        facade.place_repo.add(place2)
        facade.place_repo.add(place3)
        print("Created 3 Places")

        review1 = Review(text="Absolutely loved this place!", rating=5, user_id=user2.id, place_id=place1.id)
        review2 = Review(text="Nice, but a bit cold.", rating=4, user_id=user3.id, place_id=place1.id)
        review3 = Review(text="Noisy location.", rating=3, user_id=user3.id, place_id=place2.id)

        facade.review_repo.add(review1)
        facade.review_repo.add(review2)
        facade.review_repo.add(review3)
        print("Created 3 Reviews")

        print("Database populated successfully!")

if __name__ == "__main__":
    seed_database()