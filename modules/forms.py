from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from .models import User

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