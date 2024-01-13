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

@views.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('views.dashboard'))
    return render_template('login.html', form=form)

@views.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html')

@views.route('/logout',  methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))

@views.route('/register', methods=["GET", "POST"])
def register():
    reg_form = RegisterForm()

    if reg_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reg_form.password.data)
        new_user = User(username=reg_form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('views.login'))

    return render_template('register.html', form=reg_form)