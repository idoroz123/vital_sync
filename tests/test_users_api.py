from unittest.mock import patch
from app import app
from tests.base import ServerTestBase
from models.users import Users


class UsersApiTest(ServerTestBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_id, cls.retrieved_id = cls.initialize_db()

    @classmethod
    def initialize_db(cls):
        # Set up initial test users
        create_user = Users(
            name="test_user_exisiting",
            email="test_user_exisiting@example.com",
        )
        retrieve_user = Users(
            name="test_user_retrieved",
            email="test_user_retrieved@example.com",
        )

        with app.app_context():
            cls.session.add(create_user)
            cls.session.add(retrieve_user)
            cls.session.commit()
            return create_user.id, retrieve_user.id

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_user_success(self):
        # Test case for successful user creation
        test_data = {
            "name": "test_user",
            "email": "test@example.com",
            "age": 25,
            "gender": "Male",
            "height": 175,
            "weight": 70,
        }

        response = self.flask_test_client.post("/users", json=test_data)

        expected_data = {
            "message": "User created successfully",
            "user": {
                "name": "test_user",
                "email": "test@example.com",
                "age": 25,
                "gender": "Male",
                "height": 175,
                "weight": 70,
            },
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, expected_data)

    def test_create_user_with_existing_email_failure(self):
        # Test case for user creation failure due to an existing email
        test_data = {
            "name": "test_user_exisiting",
            "email": "test_user_exisiting@example.com",
            "age": 30,
            "gender": "Female",
            "height": 160,
            "weight": 60,
        }

        response = self.flask_test_client.post("/users", json=test_data)

        expected_data = {"error": "A user with this email already exists."}
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json, expected_data)

    def test_get_user_success(self):
        # Test case for successfully retrieving user details by ID
        response = self.flask_test_client.get(f"/users/{self.retrieved_id}")

        expected_data = {
            "user": {
                "id": self.retrieved_id,
                "name": "test_user_retrieved",
                "email": "test_user_retrieved@example.com",
                "age": 30,
                "gender": "Male",
                "height": 170,
                "weight": 65,
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_user_not_found(self):
        # Test case for retrieving a non-existent user by ID
        response = self.flask_test_client.get("/users/99999")

        expected_data = {"error": "User with ID 99999 not found."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected_data)

    def test_update_user_success(self):
        # Test case for updating user details
        test_data = {"name": "updated_name", "email": "updated@example.com", "age": 35}

        response = self.flask_test_client.put(
            f"/users/{self.retrieved_id}", json=test_data
        )

        expected_data = {
            "message": "User updated successfully",
            "user": {
                "id": self.retrieved_id,
                "name": "updated_name",
                "email": "updated@example.com",
                "age": 35,
                "gender": "Male",
                "height": 170,
                "weight": 65,
            },
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_delete_user_success(self):
        # Test case for deleting a user
        response = self.flask_test_client.delete(f"/users/{self.retrieved_id}")

        expected_data = {"message": "User deleted successfully"}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_delete_user_not_found(self):
        # Test case for trying to delete a non-existent user
        response = self.flask_test_client.delete("/users/99999")

        expected_data = {"error": "User with ID 99999 not found."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected_data)
