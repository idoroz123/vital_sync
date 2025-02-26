import pytest
from db import db
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


@pytest.mark.parametrize("category", ["sleep", "physical", "blood_tests"])
def test_create_health_data(test_client, create_user, category):
    """Test creating health data for different categories."""
    response = test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS[category])
    assert response.status_code == 201
    assert response.json["message"] == "Entry created successfully"
    assert response.json["entry"]["user_id"] == 1


@pytest.mark.parametrize("category", ["sleep", "physical", "blood_tests"])
def test_get_health_data(test_client, create_user, category):
    """Test retrieving health data for a user."""
    test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS[category])
    response = test_client.get(f"/api/health-data/{category}/1")
    assert response.status_code == 200
    assert len(response.json["entries"]) > 0


@pytest.mark.parametrize("category", ["sleep", "physical", "blood_tests"])
def test_update_health_data(test_client, create_user, category):
    """Test updating an existing health data entry."""
    res = test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS[category])
    entry_id = res.json["entry"]["id"]
    update_data = (
        {"category": category, "user_id": 1, "steps": 12000}
        if category == "physical"
        else {"user_id": 1, "sleep_quality": "average"}
    )
    response = test_client.put(
        f"/api/health-data/{category}/{entry_id}", json=update_data
    )
    assert response.status_code == 200
    assert response.json["message"] == "Entry updated successfully"


@pytest.mark.parametrize("category", ["sleep", "physical", "blood_tests"])
def test_delete_health_data(test_client, category):
    """Test deleting a health data entry."""
    res = test_client.post("/api/health-data", json=HEALTH_DATA_PAYLOADS[category])
    entry_id = res.json["entry"]["id"]
    response = test_client.delete(f"/api/health-data/{category}/{entry_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Entry deleted successfully"

    # Ensure deletion
    get_response = test_client.get(f"/api/health-data/{category}/{entry_id}")
    assert get_response.status_code == 200
    assert len(get_response.json["entries"]) == 0


def test_invalid_category(test_client):
    """Test passing an invalid category."""
    response = test_client.post(
        "/api/health-data", json={"category": "invalid", "user_id": 2}
    )
    assert response.status_code == 400
    assert "Invalid category" in response.json["error"]
