import pytest
from app import app
from db import db


@pytest.fixture(scope="module")
def test_client():
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://user:password@localhost:5432/postgres_test"
    )
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def db_fixture():
    # Set the app to use an in-memory SQLite database for testing
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://user:password@localhost:5432/postgres_test"
    )
    app.config["TESTING"] = True

    # Create a database context and bind it to the app
    with app.app_context():
        # Create all tables before each test
        db.create_all()

        yield db  # This will allow access to the db instance in your tests

        db.session.remove()  # Cleanup the session
        db.drop_all()  # Drop all tables after the test
