from flask import Flask, Blueprint, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from .db import db
from .forms import RegisterForm, LoginForm
from .models import User

views = Blueprint('views', __name__)
bcrypt = Bcrypt()

@views.route('/')
def index():
    return render_template('index.html')
