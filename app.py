from flask import Flask, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from dotenv import load_dotenv
import os

from modules.models import User
from modules.db import db
from modules.views import views
from modules.auth import auth

# create app
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

#load .env file for secret key
load_dotenv()

# tells flask-sqlalchemy what database to connect to
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# initialize sqlalchemy
db.init_app(app)

# Loginmanager for logging users in and out
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == '__main__':
    app.run(debug=True)