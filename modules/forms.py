from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from .models import User

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=24)], render_kw={"Placeholder" : "Username"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=24)], render_kw={"Placeholder" : "Password"})
    spotify_id = StringField('spotify_id', validators=[InputRequired(), Length(min=1, max=30)], render_kw={"Placeholder" : "Spotify User ID"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please sign up with a different username.")

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=24)], render_kw={"Placeholder" : "Username"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=24)], render_kw={"Placeholder" : "Password"})
    submit = SubmitField("Login")   

class SpotifyUserIDForm(FlaskForm):
    spotify_user_id = StringField('spotify_user_id', validators=[InputRequired(), Length(max=30)], render_kw={"Placeholder" : "Spotify User ID"})
    submit = SubmitField("Register Spotify User ID")

    def validate_user_id(self, spotify_user_id):
        existing_spotify_user_id = User.query.filter_by(spotify_user_id=spotify_user_id.data).first()
        if existing_spotify_user_id:
            raise ValidationError("That Spotify user ID is already registered with an account. Please try again.")