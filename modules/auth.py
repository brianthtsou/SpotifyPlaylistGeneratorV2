from flask import Blueprint, render_template, url_for, redirect, session
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt


from .db import db
from .forms import RegisterForm, LoginForm
from .models import User

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
       return render_template('dashboard.html')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    session['id'] = user.id
                    login_user(user)
                    return redirect(url_for('views.dashboard'))
        return render_template('login.html', form=form)

@auth.route('/logout',  methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=["GET", "POST"])
def register():
    reg_form = RegisterForm()

    if reg_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reg_form.password.data)
        new_user = User(username=reg_form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=reg_form)