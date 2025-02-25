import base64
import uuid
import pytest
from models.users import Users
from db import db


def generate_short_uuid():
    full_uuid = uuid.uuid4()
    # Convert the UUID to bytes and encode it in URL-safe base64 without padding
    short_uuid = base64.urlsafe_b64encode(full_uuid.bytes).rstrip(b"=").decode("utf-8")
    return short_uuid


def generate_test_email():
    return f"test-{generate_short_uuid()}@example.com"


# Sample user data with placeholder for email
USER_DATA_TEMPLATE = {
    "name": "John Doe",
    "email": "",  # Placeholder to be filled dynamically
    "age": 30,
    "gender": "male",
    "height": 175,
    "weight": 70,
}


@pytest.fixture
def user_data():
    # Create a copy of the template with a random email
    user_data = USER_DATA_TEMPLATE.copy()
    user_data["email"] = generate_test_email()
    return user_data


def test_create_user(test_client, user_data):
    response = test_client.post("/api/users", json=user_data)
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully"
    assert response.json["user"]["email"] == user_data["email"]


def test_create_user_duplicate_email(test_client, user_data):
    user_data["email"] = "duplicate_email@example.com"
    test_client.post("/api/users", json=user_data)  # Create first user
    response = test_client.post("/api/users", json=user_data)  # Attempt duplicate
    assert response.status_code == 409
    assert "A user with this email already exists." in response.json["error"]


def test_get_user(test_client, user_data):
    res = test_client.post("/api/users", json=user_data)
    print(res.json)
    user_id = res.json["user"]["id"]

    response = test_client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json["user"]["email"] == user_data["email"]


def test_get_nonexistent_user(test_client):
    response = test_client.get("/api/users/9999")  # Assuming this ID doesn't exist
    assert response.status_code == 404
    assert "User with ID 9999 not found" in response.json["error"]


def test_update_user(test_client, user_data):
    res = test_client.post("/api/users", json=user_data)
    user_id = res.json["user"]["id"]

    updated_data = {"name": "Jane Doe", "age": 35}
    response = test_client.put(f"/api/users/{user_id}", json=updated_data)

    assert response.status_code == 200
    assert response.json["user"]["name"] == "Jane Doe"
    assert response.json["user"]["age"] == 35


def test_delete_user(test_client, user_data):
    res = test_client.post("/api/users", json=user_data)
    user_id = res.json["user"]["id"]

    response = test_client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully"

    # Ensure user no longer exists
    get_response = test_client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_user(test_client):
    response = test_client.delete("/api/users/9999")  # Nonexistent user ID
    assert response.status_code == 404
    assert "User with ID 9999 not found" in response.json["error"]
