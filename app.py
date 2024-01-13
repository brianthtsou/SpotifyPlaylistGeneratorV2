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

# create app
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
#load .env file for secret key
load_dotenv()


# tells flask-sqlalchemy what database to connect to
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# initialize sqlalchemy
db.init_app(app)

# bcrypt = Bcrypt(app)

# Loginmanager for logging users in and out
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=24)], render_kw={"Placeholder" : "Username"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=24)], render_kw={"Placeholder" : "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please sign up with a different username.")

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=24)], render_kw={"Placeholder" : "Username"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=24)], render_kw={"Placeholder" : "Password"})
    submit = SubmitField("Login")   

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# @login_manager.user_loader
# def load_user(user_id):
#     return session.get(User, int(user_id))



# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/login', methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 login_user(user)
#                 return redirect(url_for('dashboard'))
#     return render_template('login.html', form=form)

# @app.route('/dashboard', methods=["GET", "POST"])
# @login_required
# def dashboard():
#     return render_template('dashboard.html')

# @app.route('/logout',  methods=["GET", "POST"])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# @app.route('/register', methods=["GET", "POST"])
# def register():
#     reg_form = RegisterForm()

#     if reg_form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(reg_form.password.data)
#         new_user = User(username=reg_form.username.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))

#     return render_template('register.html', form=reg_form)

if __name__ == '__main__':
    app.run(debug=True)