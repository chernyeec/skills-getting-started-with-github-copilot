"""Tests for the POST /activities/{activity_name}/signup endpoint using AAA pattern"""
import src.app


def test_successful_signup(app_with_activities):
    """Test that a student can successfully sign up for an activity"""
    # Arrange: Prepare test data
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    
    # Act: Send POST signup request
    response = app_with_activities.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert: Verify response and participant was added
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in src.app.activities[activity_name]["participants"]


def test_signup_to_nonexistent_activity(app_with_activities):
    """Test that signup to a nonexistent activity returns 404"""
    # Arrange: Prepare test data with nonexistent activity
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act: Send POST signup request to nonexistent activity
    response = app_with_activities.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert: Verify 404 response
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_duplicate_signup_rejected(app_with_activities):
    """Test that duplicate signup returns 400 Bad Request"""
    # Arrange: Sign up once, then prepare to signup again with same email
    activity_name = "Programming Class"
    email = "student@mergington.edu"
    app_with_activities.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act: Attempt duplicate signup
    response = app_with_activities.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert: Verify 400 response and error message
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_increments_participant_count(app_with_activities):
    """Test that signup increments the participant count"""
    # Arrange: Get initial participant count
    activity_name = "Gym Class"
    initial_count = len(src.app.activities[activity_name]["participants"])
    email = "newstudent@mergington.edu"
    
    # Act: Sign up a new participant
    app_with_activities.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert: Verify participant count increased by 1
    new_count = len(src.app.activities[activity_name]["participants"])
    assert new_count == initial_count + 1
    assert email in src.app.activities[activity_name]["participants"]
