from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PhysicalActivity(db.Model):
    __tablename__ = "physical_activity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    steps = db.Column(db.Integer, nullable=False, default=0)
    calories_burned = db.Column(db.Integer, nullable=False, default=0)
    workout_duration = db.Column(db.Numeric(4, 2), nullable=False, default=0.0)  # hours
    activity_type = db.Column(db.String(50))
    recorded_at = db.Column(db.Date, nullable=False)

    user = db.relationship("Users", backref=db.backref("physical_activity", lazy=True))
