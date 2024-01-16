from flask import session, Blueprint, url_for
from .models import User
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time

spotify = Blueprint('spotify', __name__)

user_id = session["id"]
user = User.query.filter_by(id=user_id).first()
spotify_user_id = user.spotify_user_id

""" 
Method for creating Spotify OAuth Authentication Object. The scope defines what actions the app is allowed to take on a 
user's Spotify account. 
"""
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for("redirectPage", _external=True),
        scope=("user-library-read, playlist-modify-public, user-top-read")
    )

""" 
Method for retrieving authentication token. If the token is expired, or will expire in less than 60 seconds,
the Spotify OAuth object will be recreated, and the token will be refreshed.
"""
def get_token():
    token_info = session.get("token_info", None)
    if not token_info:
        raise "Exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info

@spotify.route('/redirectpage')
def redirectPage():
    return None

