from flask_sqlalchemy import SQLAlchemy

from db import db


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    height = db.Column(db.Numeric(5, 2))  # cm
    weight = db.Column(db.Numeric(5, 2))  # kg
