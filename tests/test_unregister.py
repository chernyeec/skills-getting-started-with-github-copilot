"""Tests for the POST /activities/{activity_name}/unregister endpoint using AAA pattern"""
import src.app


def test_successful_unregister(app_with_activities):
    """Test that a participant can successfully unregister from an activity"""
    # Arrange: Sign up first, then prepare to unregister
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    app_with_activities.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act: Send POST unregister request
    response = app_with_activities.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert: Verify response and participant was removed
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in src.app.activities[activity_name]["participants"]


def test_unregister_from_nonexistent_activity(app_with_activities):
    """Test that unregister from nonexistent activity returns 404"""
    # Arrange: Prepare test data with nonexistent activity
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act: Send POST unregister request to nonexistent activity
    response = app_with_activities.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert: Verify 404 response
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_nonexistent_participant(app_with_activities):
    """Test that unregistering a nonexistent participant returns 404"""
    # Arrange: Prepare test data with email not registered in activity
    activity_name = "Programming Class"
    email = "notregistered@mergington.edu"
    
    # Act: Send POST unregister request for nonexistent participant
    response = app_with_activities.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert: Verify 404 response
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_reregister_after_unregister(app_with_activities):
    """Test that a participant can re-register after unregistering"""
    # Arrange: Sign up, unregister, then prepare to re-sign up
    activity_name = "Gym Class"
    email = "student@mergington.edu"
    app_with_activities.post(f"/activities/{activity_name}/signup?email={email}")
    app_with_activities.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Act: Re-sign up the same email
    response = app_with_activities.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert: Verify re-registration successful
    assert response.status_code == 200
    assert email in src.app.activities[activity_name]["participants"]
