from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from dotenv import load_dotenv
import os

from modules.models import User
from modules.db import db
from modules.views import views
from modules.auth import auth
from modules.spotify import spotify

# create app
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(spotify, url_prefix='/')

#load .env file for secret key
load_dotenv()

# tells flask-sqlalchemy what database to connect to
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'Spotify Playlist Generator'

# initialize sqlalchemy
db.init_app(app)

migrate = Migrate(app,db,render_as_batch=True)

# Loginmanager for logging users in and out
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == '__main__':
    app.run(debug=True)