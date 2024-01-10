from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from dotenv import load_dotenv
import os

# create app
app = Flask(__name__)

#load .env file for secret key
load_dotenv()


# tells flask-sqlalchemy what database to connect to
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# initialize sqlalchemy
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# Loginmanager for logging users in and out
login_manager = LoginManager()
login_manager.init_app(app)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(24), nullable=False)

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



# # Loginmanager for logging users in and out
# login_manager = LoginManager()
# login_manager.init_app(app)


# # Initialize app with extension
# db.init_app(app)

# # Create database within app context
# with app.app_context():
    # db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for(login))

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)