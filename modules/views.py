from flask import Blueprint, render_template, url_for, redirect, session

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')
