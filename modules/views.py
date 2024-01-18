from flask import Blueprint, render_template, redirect, session, url_for, request
from flask_login import login_required
from .db import db
from .models import User
from .forms import SpotifyUserIDForm

views = Blueprint('views', __name__)

@views.route('/')
def index():
    session.clear()
    return render_template('index.html')

@views.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    user_id = session["id"]
    user = User.query.filter_by(id=user_id).first()
    spotify_user_id = user.spotify_user_id 
    return render_template('dashboard.html', spotify_user_id=spotify_user_id)

@views.route('/account_settings', methods=["GET", "POST"])
@login_required
def account_settings():
    user_id = session["id"]
    user = User.query.filter_by(id=user_id).first()
    form = SpotifyUserIDForm()
    form.spotify_user_id.data = user.spotify_user_id 

    if form.is_submitted():
        new_user_id = request.form['spotify_user_id']
        user.spotify_user_id = new_user_id
        db.session.commit()
        return redirect(url_for('views.account_settings'))
    return render_template('account_settings.html', form=form)