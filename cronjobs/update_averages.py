from app import app
import update_system_averages

with app.app_context():
    update_system_averages()


# this cronjob would run every hour to update the system averages
# and keep the system averages up to date like this:
# 0 * * * * /path/to/venv/bin/python /path/to/update_averages.py
