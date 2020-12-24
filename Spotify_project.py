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
        self.user_albums = []
        self.user_songs = []

        self.username = sys.argv[0]
        # Erase cache and prompt for user permission
        try:
            self.token = util.prompt_for_user_token(self.username, self.scope, client_id=self.client_id,
                                               client_secret=self.client_secret,
                                               redirect_uri=self.redirect_uri)  # add scope
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{self.username}")
            self.token = util.prompt_for_user_token(self.username, self.scope)  # add scope

        self.spotifyObject = spotipy.Spotify(auth=self.token)

    def artist_song_album_helper(self, lst, data, followers_album_artist, total_or_name):
        """
        This is a helper function that will help us parse the dictionary value in the follower column for the
        top 20 artist/songs/albums function
        :param lst: this an empty list where we will append the artists followers
        :param data: this is the API dictionary that is returned when you call spotifyObject.current_user_top_artists()
        :return: the list of all 20 artists followers.
        """
        i = 0
        while len(lst) < len(data['items']):
            if followers_album_artist == 'artists':
                lst.append(data['items'][i][followers_album_artist][0][total_or_name])
            else:
                lst.append(data['items'][i][followers_album_artist][total_or_name])
            i += 1
        return lst


    def get_user_top20_artists(self):
        """
        This function will be getting the specific user top 20 most listened to artist.
        :return: Data frame the artists and different information regarding the artist.
        """
        user_data = self.spotifyObject.current_user_top_artists()
        user_items = user_data['items']
        top20_artist = pd.DataFrame.from_dict(user_items)
        top20_artist = top20_artist[['name', 'genres', 'id', 'popularity', 'followers', 'type', 'uri']]
        top20_artist['followers'] = self.artist_song_album_helper(self.artist_follower_count,
                                                                  user_data, 'followers', 'total')
        top20_artist.popularity = top20_artist.popularity.astype(int)
        top20_artist.name = top20_artist.name.astype(str)
        print(top20_artist)
        return top20_artist

    def get_users_top20_songs(self):
        top20_songs_data = self.spotifyObject.current_user_top_tracks()
        top20_songs = pd.DataFrame(top20_songs_data['items'])
        top20_songs = top20_songs[['name', 'album', 'artists',
                                         'popularity', 'duration_ms', 'explicit',
                                        'track_number', 'id', 'uri', 'preview_url']]
        song_album = self.artist_song_album_helper(self.user_albums, top20_songs_data, 'album', 'name')
        top20_songs['album'] = song_album
        song_artist = self.artist_song_album_helper(self.user_albums, top20_songs_data, 'artists', 'name')
        top20_songs['artists'] = song_artist
        print(top20_songs)
        return top20_songs

# TODO: spotifyObject.current_user_playlists() can retrieve all the users made playlists
# another idea can be creating a tool where you can keep track of the playlists you have on spotify
# Only info im seeing that I can get from that function is the amount of songs each playlist has.


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--string_input", type=str, default=None)

    args = parser.parse_args()
    Spotify_User = SpotifyData(args)
    #Spotify_User.get_user_top20_artists()
    Spotify_User.get_users_top20_songs()