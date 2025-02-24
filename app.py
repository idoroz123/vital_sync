import os
from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
server_env = os.environ.get("SERVER_ENV", "Test")
app.config.from_object("config.{server_env}".format(server_env=server_env))
db = SQLAlchemy(app)

from models.users import Users
from models.blood_tests import BloodTests
from models.health_scores import HealthScores
from models.physical_activity import PhysicalActivity
from models.sleep_activity import SleepActivity

from schemas.users import UserCreate, UserUpdate

with app.app_context():
    db.create_all()
