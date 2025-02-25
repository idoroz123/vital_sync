import pytest
from app import app
from db import db


@pytest.fixture
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
