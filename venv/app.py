from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# create app
app = Flask(__name__)

#load .env file for secret key
load_dotenv()

# tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = os.getenv("SECRET_KEY")


@app.route('/', methods=['GET'])
