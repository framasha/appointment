import os
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointment.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/appointmentdb'
db = SQLAlchemy(app)

from routes import *

if __name__ == "__main__":
    app.run(debug=True)