import os
from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
server_env = os.environ.get("SERVER_ENV", "Test")
app.config.from_object("config.{server_env}".format(server_env=server_env))
db = SQLAlchemy(app)


with app.app_context():
    db.create_all()
