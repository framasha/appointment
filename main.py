import os
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ACCESS_EXPIRES = datetime.timedelta(hours=int(os.environ.get("ACCESS_EXPIRES")))
# REFRESH_EXPIRES = datetime.timedelta(hours=int(os.environ.get("REFRESH_EXPIRES")))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
# app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
# app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

from routes import *

if __name__ == "__main__":
    app.run(debug=True)