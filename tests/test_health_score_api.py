import pytest
from app import app
from db import db
from models.sleep_activity import SleepActivity
from models.physical_activity import PhysicalActivity
from models.blood_tests import BloodTests
from models.system_averages import SystemAverages
from api.exceptions import UserNotFoundError
from models.users import Users

# Sample data for testing
HEALTH_DATA_PAYLOADS = {
    "sleep": {
        "category": "sleep",
        "total_sleep_duration": 7.5,
        "sleep_quality": "Good",
        "deep_sleep_duration": 2.5,
        "wake_up_count": 1,
        "recorded_at": "2024-02-25",
        "user_id": 1,
    },
    "physical": {
        "category": "physical",
        "user_id": 1,
        "steps": 10000,
        "calories_burned": 500,
        "workout_duration": 1.5,
        "activity_type": "Running",
        "recorded_at": "2024-02-25",
    },
    "blood_tests": {
        "category": "blood_tests",
        "user_id": 1,
        "cholesterol": 180,
        "hemoglobin": 15,
        "glucose_level": 100,
        "triglycerides": 150,
        "blood_pressure": "120/80",
        "test_date": "2024-02-25",
    },
}


@pytest.fixture(scope="module")
def create_user(test_client):
    """Fixture to create a user with id 1 for testing."""
    user = Users(
        id=1,
        name="Test User",
        email="testuser@example.com",
        age=30,
        gender="M",
        height=175,
        weight=70,
    )
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()


@pytest.fixture
def system_averages():
    # Setup system averages
    system_avg = SystemAverages(
        avg_sleep_duration=7.0, avg_steps=8000, avg_glucose_level=85
    )
    db.session.add(system_avg)
    db.session.commit()


def test_get_health_score_with_data(test_client, create_user, system_averages):
    """Test health score calculation with data and system averages."""
    _ = test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS["sleep"])
    _ = test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS["sleep"])
    _ = test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS["physical"])
    response = test_client.get("api/get_health_score/1")

    assert response.status_code == 200
    json_data = response.get_json()
    assert "health_score" in json_data
    assert "details" in json_data
    assert json_data["health_score"] > 0
    assert json_data["details"]["sleep_score"] > 0
    assert json_data["details"]["steps_score"] > 0
    assert json_data["details"]["glucose_score"] > 0


def test_get_health_score_user_doesnt_exist(test_client):
    with pytest.raises(UserNotFoundError):
        _ = test_client.get("/api/get_health_score/999")


def test_health_score_format(test_client, create_user, system_averages):
    """Test the response format for health score calculation."""
    _ = test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS["sleep"])
    _ = test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS["sleep"])
    _ = test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS["physical"])
    response = test_client.get("/api/get_health_score/1")

    assert response.status_code == 200
    json_data = response.get_json()

    assert isinstance(json_data, dict)
    assert "health_score" in json_data
    assert isinstance(json_data["health_score"], float)
    assert "details" in json_data
    assert isinstance(json_data["details"], dict)
    assert "sleep_score" in json_data["details"]
    assert "steps_score" in json_data["details"]
    assert "glucose_score" in json_data["details"]
