"""Tests for the GET /activities endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_get_activities_returns_all_activities(app_with_activities):
    """Test that GET /activities returns all activities"""
    # Arrange: app_with_activities fixture provides TestClient with fresh activities
    
    # Act: Send GET request to /activities endpoint
    response = app_with_activities.get("/activities")
    
    # Assert: Verify response status and content
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_returns_correct_structure(app_with_activities):
    """Test that each activity has the required fields"""
    # Arrange: app_with_activities fixture provides TestClient with fresh activities
    
    # Act: Send GET request to /activities endpoint
    response = app_with_activities.get("/activities")
    
    # Assert: Verify each activity has required fields
    activities = response.json()
    for activity_name, details in activities.items():
        assert "description" in details, f"{activity_name} missing 'description'"
        assert "schedule" in details, f"{activity_name} missing 'schedule'"
        assert "max_participants" in details, f"{activity_name} missing 'max_participants'"
        assert "participants" in details, f"{activity_name} missing 'participants'"
        assert isinstance(details["participants"], list), f"{activity_name} participants not a list"


def test_root_redirects_to_static_index(app_with_activities):
    """Test that GET / redirects to /static/index.html"""
    # Arrange: app_with_activities fixture provides TestClient with fresh activities
    
    # Act: Send GET request to root without following redirects
    response = app_with_activities.get("/", follow_redirects=False)
    
    # Assert: Verify redirect status and location header
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
