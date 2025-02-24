from flask_sqlalchemy import SQLAlchemy

from app import db


class HealthScores(db.Model):  # Optional caching table
    __tablename__ = "health_scores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    score = db.Column(db.Numeric(5, 2), nullable=False)
    calculated_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    user = db.relationship("Users", backref=db.backref("health_scores", lazy=True))
