from db import db
from models.system_averages import SystemAverages
from models.sleep_activity import SleepActivity
from models.physical_activity import PhysicalActivity
from models.blood_tests import BloodTests
from sqlalchemy.sql import func


def update_system_averages():
    """Recalculates system-wide health data averages and updates the SystemAverages table."""

    # Fetch current or create new SystemAverages record
    system_avg = db.session.query(SystemAverages).first()
    if not system_avg:
        system_avg = SystemAverages()
        db.session.add(system_avg)

    # Sleep Averages
    system_avg.avg_sleep_duration = (
        db.session.query(func.avg(SleepActivity.total_sleep_duration)).scalar() or 0
    )
    system_avg.avg_deep_sleep_duration = (
        db.session.query(func.avg(SleepActivity.deep_sleep_duration)).scalar() or 0
    )
    system_avg.avg_wake_up_count = (
        db.session.query(func.avg(SleepActivity.wake_up_count)).scalar() or 0
    )

    # Physical Activity Averages
    system_avg.avg_steps = (
        db.session.query(func.avg(PhysicalActivity.steps)).scalar() or 0
    )
    system_avg.avg_calories_burned = (
        db.session.query(func.avg(PhysicalActivity.calories_burned)).scalar() or 0
    )
    system_avg.avg_workout_duration = (
        db.session.query(func.avg(PhysicalActivity.workout_duration)).scalar() or 0
    )

    # Blood Test Averages
    system_avg.avg_glucose_level = (
        db.session.query(func.avg(BloodTests.glucose_level)).scalar() or 0
    )
    system_avg.avg_cholesterol_level = (
        db.session.query(func.avg(BloodTests.cholesterol)).scalar() or 0
    )
    system_avg.avg_blood_pressure = (
        db.session.query(func.avg(BloodTests.blood_pressure)).scalar() or 0
    )

    # Commit the updates
    db.session.commit()
