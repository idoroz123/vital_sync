from decimal import Decimal
from flask import Blueprint, request, jsonify
from sqlalchemy.sql import func
from db import db
from models.sleep_activity import SleepActivity
from models.physical_activity import PhysicalActivity
from models.blood_tests import BloodTests
from schemas.health_score import HealthScoreResponse
from api.exceptions import UserNotFoundError
from models.system_averages import SystemAverages

health_score_api = Blueprint("health_score_api", __name__)


@health_score_api.route("/get_health_score/<int:user_id>", methods=["GET"])
def get_health_score(user_id):
    # Fetch user data
    user_sleep = db.session.query(SleepActivity).filter_by(user_id=user_id).all()
    user_physical = db.session.query(PhysicalActivity).filter_by(user_id=user_id).all()
    user_blood_tests = db.session.query(BloodTests).filter_by(user_id=user_id).all()

    if not (user_sleep or user_physical or user_blood_tests):
        raise UserNotFoundError(f"No health data found for user {user_id}")

    # Fetch system averages (or use default logic if not available)
    system_averages = (
        db.session.query(SystemAverages).order_by(SystemAverages.id.desc()).first()
    )

    if not system_averages:
        # Fallback to calculating averages across all users if system averages are not available
        avg_sleep = (
            db.session.query(func.avg(SleepActivity.total_sleep_duration)).scalar() or 0
        )
        avg_steps = db.session.query(func.avg(PhysicalActivity.steps)).scalar() or 0
        avg_glucose = db.session.query(func.avg(BloodTests.glucose_level)).scalar() or 0
    else:
        # Use system averages if available
        avg_sleep = system_averages.avg_sleep_duration
        avg_steps = system_averages.avg_steps
        avg_glucose = system_averages.avg_glucose_level

    # Get user's latest entries
    latest_sleep = user_sleep[-1] if user_sleep else None
    latest_physical = user_physical[-1] if user_physical else None
    latest_blood_test = user_blood_tests[-1] if user_blood_tests else None

    # Normalize values (1 if no data)
    sleep_score = (
        (Decimal(latest_sleep.total_sleep_duration) / Decimal(avg_sleep))
        if latest_sleep
        else 1
    )
    steps_score = (
        (Decimal(latest_physical.steps) / Decimal(avg_steps)) if latest_physical else 1
    )
    glucose_score = (
        (Decimal(avg_glucose) / Decimal(latest_blood_test.glucose_level))
        if latest_blood_test
        else 1
    )

    # Weighted health score formula
    health_score = (
        (Decimal(sleep_score) * Decimal(0.4))
        + (Decimal(steps_score) * Decimal(0.4))
        + (Decimal(glucose_score) * Decimal(0.2))
    )
    health_score = round(health_score * 100, 2)  # Scale to percentage

    response = HealthScoreResponse(
        user_id=user_id,
        health_score=health_score,
        details={
            "sleep_score": round(sleep_score, 2),
            "steps_score": round(steps_score, 2),
            "glucose_score": round(glucose_score, 2),
        },
    )

    return jsonify(response.model_dump()), 200
