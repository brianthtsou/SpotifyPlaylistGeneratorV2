from flask import Blueprint, render_template, redirect, session, url_for
from flask_login import login_required
from .db import db
from .models import User
from .forms import SpotifyUserIDForm

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html')

@views.route('/account_settings', methods=["GET", "POST"])
@login_required
def account_settings():
    form = SpotifyUserIDForm()

    if form.is_submitted():
        user_id = session["id"]
        user = User.query.filter_by(id=user_id).first()
        user.spotify_user_id = form.spotify_user_id.data
        db.session.commit()
        return redirect(url_for('views.account_settings'))
    return render_template('account_settings.html', form=form)