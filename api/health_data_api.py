from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.sleep_activity import SleepActivity
from models.physical_activity import PhysicalActivity
from models.blood_tests import BloodTests
from api.exceptions import ValidationError, DatabaseError, UserNotFoundError
from schemas.blood_tests import BloodTestCreate, BloodTestUpdate, BloodTestResponse
from schemas.sleep_activity import (
    SleepActivityCreate,
    SleepActivityUpdate,
    SleepActivityResponse,
)
from schemas.physical_activity import (
    PhysicalActivityCreate,
    PhysicalActivityUpdate,
    PhysicalActivityResponse,
)
from schemas.blood_tests import BloodTestCreate, BloodTestUpdate, BloodTestResponse

health_data_api = Blueprint("health_data_api", __name__)


CATEGORY_MODELS = {
    "sleep": (
        SleepActivity,
        SleepActivityCreate,
        SleepActivityUpdate,
        SleepActivityResponse,
    ),
    "physical": (
        PhysicalActivity,
        PhysicalActivityCreate,
        PhysicalActivityUpdate,
        PhysicalActivityResponse,
    ),
    "blood_tests": (BloodTests, BloodTestCreate, BloodTestUpdate, BloodTestResponse),
}


def get_model_and_schemas(category):
    if category not in CATEGORY_MODELS:
        raise ValidationError(f"Invalid category: {category}")
    return CATEGORY_MODELS[category]


@health_data_api.route("/health-data", methods=["POST"])
def create_health_data():
    try:
        data = request.get_json()
        category = data.get("category")
        user_id = data.get("user_id")
        model, create_schema, _, response_schema = get_model_and_schemas(category)

        validated_data = create_schema(**data)  # Validate with Pydantic

        new_entry = model(user_id=user_id, **validated_data.model_dump())
        db.session.add(new_entry)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Entry created successfully",
                    "entry": response_schema.model_validate(new_entry).model_dump(),
                }
            ),
            201,
        )

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "A database error occurred"}), 500


@health_data_api.route("/health-data/<category>/<int:user_id>", methods=["GET"])
def get_health_data(category, user_id):
    try:
        model, _, _, response_schema = get_model_and_schemas(category)
        entries = model.query.filter_by(user_id=user_id).all()

        return (
            jsonify(
                {
                    "entries": [
                        response_schema.model_validate(entry).model_dump()
                        for entry in entries
                    ]
                }
            ),
            200,
        )
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError:
        return jsonify({"error": "A database error occurred"}), 500


@health_data_api.route("/health-data/<category>/<int:entry_id>", methods=["PUT"])
def update_health_data(category, entry_id):
    try:
        model, _, update_schema, response_schema = get_model_and_schemas(category)
        entry = model.query.get(entry_id)
        if not entry:
            raise UserNotFoundError(f"Entry with ID {entry_id} not found")

        data = request.get_json()
        validated_data = update_schema(**data)  # Validate update data

        for key, value in validated_data.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)

        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Entry updated successfully",
                    "entry": response_schema.model_validate(entry).model_dump(),
                }
            ),
            200,
        )

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "A database error occurred"}), 500


@health_data_api.route("/health-data/<category>/<int:entry_id>", methods=["DELETE"])
def delete_health_data(category, entry_id):
    try:
        model, _, _, _ = get_model_and_schemas(category)
        entry = model.query.get(entry_id)
        if not entry:
            raise UserNotFoundError(f"Entry with ID {entry_id} not found")

        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Entry deleted successfully"}), 200

    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "A database error occurred"}), 500
