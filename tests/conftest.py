import pytest
from app import app
from db import db


@pytest.fixture(scope="module")
def test_client():
    """Creates a test client and sets up the test database (once per module)."""
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://user:password@localhost:5432/postgres_test"
    )
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()  # Provide the test client

        db.session.remove()
        db.drop_all()  # Cleanup after all tests in the module


@pytest.fixture(scope="function")
def db_fixture():
    """Ensures each test starts with a clean database state."""
    with app.app_context():
        db.session.begin_nested()  # Use nested transactions for rollback

        yield db  # Provide the db instance

        db.session.rollback()  # Rollback any changes made in the test
