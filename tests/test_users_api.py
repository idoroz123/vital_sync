import pytest
from models.users import Users
from db import db

# Sample user data
USER_DATA = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "gender": "male",
    "height": 175,
    "weight": 70,
}


def test_create_user(test_client):
    """Test user creation"""
    response = test_client.post("/api/users", json=USER_DATA)
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully"
    assert response.json["user"]["email"] == USER_DATA["email"]


def test_create_user_duplicate_email(test_client):
    """Test creating a user with an existing email"""
    test_client.post("/api/users", json=USER_DATA)  # Create first user
    response = test_client.post("/api/users", json=USER_DATA)  # Attempt duplicate
    assert response.status_code == 409
    assert "A user with this email already exists." in response.json["error"]


def test_get_user(test_client):
    """Test retrieving a user"""
    res = test_client.post("/api/users", json=USER_DATA)
    user_id = res.json["user"]["id"]

    response = test_client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json["user"]["email"] == USER_DATA["email"]


def test_get_nonexistent_user(test_client):
    """Test retrieving a non-existent user"""
    response = test_client.get("/api/users/9999")  # Assuming this ID doesn't exist
    assert response.status_code == 404
    assert "User with ID 9999 not found" in response.json["error"]


def test_update_user(test_client):
    """Test updating a user's details"""
    res = test_client.post("/api/users", json=USER_DATA)
    user_id = res.json["user"]["id"]

    updated_data = {"name": "Jane Doe", "age": 35}
    response = test_client.put(f"/api/users/{user_id}", json=updated_data)

    assert response.status_code == 200
    assert response.json["user"]["name"] == "Jane Doe"
    assert response.json["user"]["age"] == 35


def test_delete_user(test_client):
    """Test deleting a user"""
    res = test_client.post("/api/users", json=USER_DATA)
    user_id = res.json["user"]["id"]

    response = test_client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully"

    # Ensure user no longer exists
    get_response = test_client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_user(test_client):
    """Test deleting a user that does not exist"""
    response = test_client.delete("/api/users/9999")  # Nonexistent user ID
    assert response.status_code == 404
    assert "User with ID 9999 not found" in response.json["error"]
