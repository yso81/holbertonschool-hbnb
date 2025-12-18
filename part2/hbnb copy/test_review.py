#!/usr/bin/python3
from app.models.review import Review

def test_review_creation():
    """
    Tests the creation of a Review instance.
    """
    # Create a new review instance with sample data
    review = Review(
        user_id="user123",
        place_id="place456",
        rating=5,
        text="This was a fantastic experience!"
    )

    # Assert that the instance attributes are set correctly
    assert review.user_id == "user123"
    assert review.place_id == "place456"
    assert review.rating == 5
    assert review.text == "This was a fantastic experience!"

    print("Review creation test passed!")

# Execute the test function
test_review_creation()