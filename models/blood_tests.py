from flask_sqlalchemy import SQLAlchemy

from app import db


class BloodTests(db.Model):
    __tablename__ = "blood_tests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    glucose_level = db.Column(db.Numeric(5, 2))
    cholesterol = db.Column(db.Numeric(5, 2))
    hemoglobin = db.Column(db.Numeric(5, 2))
    blood_pressure = db.Column(db.String(10))  # Stored as "120/80"
    triglycerides = db.Column(db.Numeric(5, 2))
    test_date = db.Column(db.Date, nullable=False)

    user = db.relationship("Users", backref=db.backref("blood_tests", lazy=True))
