from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from dotenv import load_dotenv
import os

# create app
app = Flask(__name__)

#load .env file for secret key
load_dotenv()

# tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = os.getenv("SECRET_KEY")

# Loginmanager for logging users in and out
login_manager = LoginManager()
login_manager.init_app(app)

# initialize sqlalchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(24), unique=True, nullable=False)

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
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)