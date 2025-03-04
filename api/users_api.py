from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas.users import UserCreate, UserResponse, UserUpdate
from api.exceptions import (
    UserNotFoundError,
    ValidationError,
    UserAlreadyExistsError,
    DatabaseError,
)
from models.users import Users

user_api = Blueprint("user_api", __name__)


def validate_user_data(data, user_type="create"):
    try:
        if user_type == "create":
            return UserCreate(**data)
        elif user_type == "update":
            return UserUpdate(**data)
    except ValidationError as e:
        raise ValidationError(f"Validation error: {e}")


def get_user_by_id(user_id):
    user = db.session.query(Users).filter_by(id=user_id).first()
    if user is None:
        raise UserNotFoundError(f"User with ID {user_id} not found.")
    return user


def check_user_exists_by_email(email):
    if db.session.query(Users).filter_by(email=email).first():
        raise UserAlreadyExistsError("A user with this email already exists.")


def commit_to_db():
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise Exception("A database error occurred")


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
        db.session.refresh(new_user)  # Ensure the new_user object gets its ID

        user_response = UserResponse.model_validate(new_user)

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "user": user_response.model_dump(),
                }
            ),
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


@user_api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = get_user_by_id(user_id)
        user_response = UserResponse.model_validate(user)
        return jsonify({"user": user_response.model_dump()}), 200

    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_api.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        user_update = validate_user_data(data, user_type="update")

        user = get_user_by_id(user_id)

        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        commit_to_db()

        user_response = UserResponse.model_validate(user)

        return (
            jsonify(
                {
                    "message": "User updated successfully",
                    "user": user_response.model_dump(),
                }
            ),
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
