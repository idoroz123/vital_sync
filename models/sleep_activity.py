from flask_sqlalchemy import SQLAlchemy

from db import db


class SleepActivity(db.Model):
    __tablename__ = "sleep_activity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_sleep_duration = db.Column(db.Numeric(4, 2), nullable=False)
    sleep_quality = db.Column(db.String(50), nullable=False)
    deep_sleep_duration = db.Column(db.Numeric(4, 2), nullable=False)
    wake_up_count = db.Column(db.Integer, nullable=False, default=0)
    recorded_at = db.Column(db.Date, nullable=False)

    user = db.relationship("Users", backref=db.backref("sleep_activity", lazy=True))
