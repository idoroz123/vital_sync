# user_api.py

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from schemas.users import UserCreate, UserUpdate
from api.exceptions import (
    UserNotFoundError,
    ValidationError,
    UserAlreadyExistsError,
    DatabaseError,
)
from app import db
from models.users import Users  # Import the Users model

user_api = Blueprint("user_api", __name__)


# Helper function to validate user input
def validate_user_data(data, user_type="create"):
    try:
        if user_type == "create":
            return UserCreate(**data)
        elif user_type == "update":
            return UserUpdate(**data)
    except ValidationError as e:
        raise ValidationError(f"Validation error: {e}")


# Helper function to get user by ID
def get_user_by_id(user_id):
    user = db.session.query(Users).filter_by(id=user_id).first()
    if user is None:
        raise UserNotFoundError(f"User with ID {user_id} not found.")
    return user


# Helper function to check if user already exists by email
def check_user_exists_by_email(email):
    if db.session.query(Users).filter_by(email=email).first():
        raise UserAlreadyExistsError("A user with this email already exists.")


# Helper function for committing changes to DB
def commit_to_db():
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise Exception("A database error occurred")


# Create User
@user_api.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        user = validate_user_data(data, user_type="create")
        check_user_exists_by_email(user.email)

        new_user = Users(
            name=user.name,
            email=user.email,
            age=user.age,
            gender=user.gender,
            height=user.height,
            weight=user.weight,
        )

        db.session.add(new_user)
        commit_to_db()

        return (
            jsonify({"message": "User created successfully", "user": user.dict()}),
            201,
        )

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except UserAlreadyExistsError as e:
        return jsonify({"error": str(e)}), 409
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Read User
@user_api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = get_user_by_id(user_id)
        return jsonify({"user": user.to_dict()}), 200

    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Update User
@user_api.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        user_update = validate_user_data(data, user_type="update")

        user = get_user_by_id(user_id)

        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)

        commit_to_db()

        return (
            jsonify({"message": "User updated successfully", "user": user.to_dict()}),
            200,
        )

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Delete User
@user_api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = get_user_by_id(user_id)

        db.session.delete(user)
        commit_to_db()

        return jsonify({"message": "User deleted successfully"}), 200

    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
