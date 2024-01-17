from flask import session, Blueprint, url_for, request, redirect, render_template
from .models import User
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time
from datetime import date

spotify = Blueprint('spotify', __name__)

load_dotenv()

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


"""
A method that parses for track name and artist name from JSON file retrieved from Spotify API, returning a dictionary
of the user's top tracks and their associated artists.
"""
def get_top_tracks_and_artists(num, result):
    #result = json file from spotify
    final_list = {}
    for track in range(num):
        artist_list = result['items'][track]['artists']
        artists = []
        for artist in range(len(artist_list)):
            artists.append(artist_list[artist]["name"])

        all_artists = ', '.join(artists) #in case of multiple artists, all need to be on one string

        track_name = str(result['items'][track]['name'])
        final_list[track_name] = all_artists
    return final_list

"""
Method for providing the redirect_uri route for the Spotify OAuth authentication object (created by create_spotify_auth()).
"""
@spotify.route('/redirectpage')
def redirect_page():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for("views.dashboard"), external=True)

"""
Method that provides the route to access the Spotify website directly to authenticate the app's connection to Spotify.
"""
@spotify.route('/spotify_login')
def spotify_login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

"""
Method that invokes get_top_tracks_and_artists() to retrieve and display user's most listened to tracks, with provided number of 
tracks and scope.
"""
@spotify.route('/get_top_tracks', methods=['GET'])
def get_top_tracks(scope="", num=0):
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for("spotify_login", _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    global current_top_track_scope

    # num = 5 by default, 10/15/20 by user selection
    # scope = short_term by default, medium_term/long_term by user selection
    num = int(request.args.get('num'))
    scope = str(request.args.get('scope'))
    current_top_track_scope = scope

    # retrieve (limit) number of top tracks as a json, stored in result
    result = sp.current_user_top_tracks(limit=num, offset=0, time_range=scope)
    
    final_list = get_top_tracks_and_artists(num=num, result=result) # for storing final 'song' : 'artist' dictionary
    return render_template('dashboard.html', tracks = final_list, current_scope = scope)

"""
Method to create an empty playlist on the user's Spotify account.
"""
@spotify.route('/create_empty_playlist')
def create_empty_playlist():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for("spotify_login", _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.user_playlist_create(spotify_user_id, "New Playlist", public=True, collaborative=False, description="blank")
    return None# render_template('playlistCreated.html')



"""
Method to generate a new playlist of songs on the user's Spotify account using the user's top listened to songs as 
recommendation seeds.
"""
@spotify.route('/create_discovery_playlist')
def create_discovery_playlist():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for("spotify_login", _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    today = str(date.today())
    sp.user_playlist_create(spotify_user_id, f"Discovery - {today}", public=True, collaborative=False, description=f"{today}")

    #gets newly created playlist (0 index is the playlist that was just created)
    discovery_playlist_id = sp.current_user_playlists(limit=1, offset=0)["items"][0]["id"]
    print(discovery_playlist_id)


    seed_tracklist = [] #list to hold seeds for recommendation function
    
    # pulls 20 short term top tracks from spotify as json, use as recommend function seeds
    result = sp.current_user_top_tracks(limit=5, offset=0, time_range="short_term")
    for track in range(5):
        track_id = result['items'][track]['id']
        seed_tracklist.append(track_id)

    # retrieves recommended tracks
    discovery_list = sp.recommendations(seed_tracks=seed_tracklist, limit=20)
    add_tracklist = [] #tracklist to be added to the playlist
    for track in range(20):
        track_id = discovery_list['tracks'][track]['id']
        add_tracklist.append(track_id)
        print(track_id)
    # TODO: need to store tracks in a list to be added
    #TODO: need to get playlist ID of newly created playlist, so can call user_playlist_add_tracks
    sp.user_playlist_add_tracks(spotify_user_id, discovery_playlist_id, add_tracklist)
    #TODO: consolidate some of these actions into separate functions
    return None # render_template('playlistCreated.html')