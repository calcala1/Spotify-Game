import sys
import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import tekore as tk


class SpotifyData:
    def __init__(self, args):
        self.args = args
        self.client_id = 'af28105a036740e4a2ca1a24959d191b'
        self.client_secret = '93324fd249d84c72995285e6899eb56b'
        self.redirect_uri = 'http://localhost:8888/callback/'
        self.scope = 'user-read-private user-read-playback-state user-modify-playback-state user-top-read ' \
                'playlist-modify-public playlist-read-collaborative '


    def get_artist_info(self):
        username = sys.argv[0]
        # Erase cache and prompt for user permission
        liluzi_uri = 'spotify:artist:4O15NlyKLIASxsJ0PrXPfz'
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client_id,
                                                                   client_secret=self.client_secret))
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret))

        results = spotify.artist_albums(liluzi_uri,album_type='album')
        albums = results['items']
        while results['next']:
            results = spotify.next(results)
            albums.extend(results['items'])
        for album in albums:
            print(album['name'])

    def get_user_info(self):
        conf = (self.client_id, self.client_secret, self.redirect_uri)
        token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)

        spotify = tk.Spotify(token)
        tracks = spotify.current_user_top_tracks(limit=10)
        current_spotify_user = spotify.current_user()
        print(current_spotify_user)
        print(tracks)
        print('hi')
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--string_input", type=str, default=None)

    args = parser.parse_args()
    the_class = SpotifyData(args)
    the_class.get_user_info()
    the_class.get_artist_info()