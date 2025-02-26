from db import db


class SystemAverages(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Sleep averages
    avg_sleep_duration = db.Column(db.Float, nullable=False, default=0)
    avg_deep_sleep_duration = db.Column(db.Float, nullable=False, default=0)
    avg_wake_up_count = db.Column(db.Float, nullable=False, default=0)

    # Physical activity averages
    avg_steps = db.Column(db.Float, nullable=False, default=0)
    avg_calories_burned = db.Column(db.Float, nullable=False, default=0)
    avg_workout_duration = db.Column(db.Float, nullable=False, default=0)

    # Blood test averages
    avg_glucose_level = db.Column(db.Float, nullable=False, default=0)
    avg_cholesterol_level = db.Column(db.Float, nullable=False, default=0)
    avg_blood_pressure = db.Column(db.Float, nullable=False, default=0)
