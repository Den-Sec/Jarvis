#!/usr/bin/env python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve Spotify credentials and device ID from environment variables
DEVICE_ID = os.getenv("DEVICE_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state"
))

def play_item_by_name_and_artist(query, artist_name=None):
    # Search for tracks and playlists by query
    results = sp.search(q=query, limit=10, type='track,playlist')

    # Check if any tracks were found
    if results['tracks']['items']:
        for track in results['tracks']['items']:
            if artist_name:
                for artist in track['artists']:
                    if artist_name.lower() in artist['name'].lower():
                        # Found the track with matching artist
                        track_uri = track['uri']
                        
                        # Transfer playback to the specified device
                        sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

                        # Play the specified Spotify track
                        sp.start_playback(device_id=DEVICE_ID, uris=[track_uri])
                        return
            else:
                # If no artist name is provided, play the first matching track
                track_uri = track['uri']
                sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                sp.start_playback(device_id=DEVICE_ID, uris=[track_uri])
                return

    # Check if any playlists were found
    if results['playlists']['items']:
        playlist_uri = results['playlists']['items'][0]['uri']
        
        # Transfer playback to the specified device
        sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

        # Play the specified Spotify playlist
        sp.start_playback(device_id=DEVICE_ID, context_uri=playlist_uri)
        return

    print("No tracks or playlists found matching the given query.")
