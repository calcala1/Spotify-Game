import sys
import argparse
import spotipy
import os
from json.decoder import JSONDecodeError
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import tekore as tk
import json
import pandas as pd

"""
The game that I could potentially build is creating a game where users can guess their favorite artists/songs from 
ascending order. This could be like guess your top 15 favorite artists/songs on spotify.
"""

class SpotifyData:
    def __init__(self, args):
        self.args = args
        # You have to set these personal variables as env-variables for now (for security reasons that way no one sees
        # your info)
        self.client_id = os.environ['SPOTIPY_CLIENT_ID']
        self.client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
        self.redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']
        self.scope = 'user-read-private user-read-playback-state user-modify-playback-state user-top-read ' \
                'playlist-modify-public playlist-read-collaborative '
        self.artist_follower_count = []

    def get_artist_follower_number(self, lst, data):
        i = 0
        while len(lst) < len(data['items']):
            lst.append(data['items'][i]['followers']['total'])
            i += 1
        return lst

    def get_user_top20_artists(self):
        username = sys.argv[0]
        scope = 'user-read-private user-read-playback-state user-modify-playback-state user-top-read playlist-modify-public playlist-read-collaborative'

        # Erase cache and prompt for user permission
        try:
            token = util.prompt_for_user_token(username, scope, client_id=self.client_id,
                                               client_secret=self.client_secret,
                                               redirect_uri=self.redirect_uri)  # add scope
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope)  # add scope

        spotifyObject = spotipy.Spotify(auth=token)

        user_data = spotifyObject.current_user_top_artists()
        user_items = user_data['items']
        top20_artist = pd.DataFrame.from_dict(user_items)
        top20_artist = top20_artist[['name', 'genres', 'id', 'popularity', 'followers', 'type', 'uri']]
        top20_artist['followers'] = self.get_artist_follower_number(self.artist_follower_count, user_data)
        top20_artist.popularity = top20_artist.popularity.astype(int)
        top20_artist.name = top20_artist.name.astype(str)
        # TODO should pass this df in memory? (most likely we will)

        print(top20_artist)
# TODO this function is to be fixed and completely refactored to get top 20 songs...
    def get_user_info(self):
        conf = (self.client_id, self.client_secret, self.redirect_uri)
        token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)

        spotify = tk.Spotify(token)
        tracks = spotify.current_user_top_tracks(time_range='long_term',limit=50,offset=0)
        for song in range(50):
            list = []
            list.append(tracks)
            with open('/Users/christianalcala/top50_data.json', 'w', encoding='utf-8') as f:
                json.dump(list, f, ensure_ascii=False, indent=4)

        current_spotify_user = spotify.current_user()
        print(current_spotify_user.id)
        print(tracks)
        print('hi')
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--string_input", type=str, default=None)

    args = parser.parse_args()
    the_class = SpotifyData(args)
    the_class.get_user_top20_artists()