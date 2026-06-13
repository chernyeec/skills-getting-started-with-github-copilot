import pytest
from fastapi.testclient import TestClient
import src.app


@pytest.fixture
def client():
    """Return a TestClient for the FastAPI app"""
    return TestClient(src.app.app)


@pytest.fixture
def fresh_activities():
    """Return a fresh activities dictionary for each test"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": []
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }


@pytest.fixture
def app_with_activities(fresh_activities):
    """Inject fresh activities into the app for each test"""
    src.app.activities = fresh_activities
    return TestClient(src.app.app)
