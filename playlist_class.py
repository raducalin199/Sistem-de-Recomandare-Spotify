import numpy as np
import pandas as pd
import seaborn as sns
import spotipy
import spotipy.util as util

CLIENT_ID = "0917f4abdf274b6db3264f55485d66e2"
CLIENT_SECRET = "7c5f26d4e6744c63952c8f28bc7246dc"
PLAY_CREATE, PLAY_ID= ["Radu.calin","2WXbUj2JMR1pDSOLhbsTIp"]


def convert_to_csv(playlist_df):
    playlist_df.drop(
        columns=["artist", "album", "track_name", "popularity", "mode", "key", "duration_ms", "time_signature"]).to_csv(
        "date_X.csv")
    playlist_df.filter(['artist', 'album', 'track_name']).to_csv("date_y.csv")


class PLAY:
    def __init__(self, client_id = CLIENT_ID, creator=PLAY_CREATE, client_secret=CLIENT_SECRET, playlist_id=PLAY_ID):
        self.client_id = client_id
        self.creator= creator
        self.client_secret = client_secret
        self.playlist_id = playlist_id

        token = util.spotipy.oauth2.SpotifyClientCredentials(client_id=self.client_id,
                                                              client_secret=self.client_secret)
        cache_token = token.get_access_token(as_dict=False)
        self.sp = spotipy.Spotify(cache_token)


    def get_playlist_tracks(self, sp):
        results = self.sp.user_playlist_tracks(self.creator, self.playlist_id)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        return tracks


    def analiza_playlist( self, creator,  playlist_id):
    # Creeam un tablou de date
        playlist_features_list = ["artist", "album", "track_name", "release_date", "popularity", "track_id",
                                       "danceability", "energy", "key", "loudness", "mode", "speechiness",
                                       "instrumentalness", "liveness", "valence", "tempo", "duration_ms",
                                       "time_signature"]

        playlist_df = pd.DataFrame(columns=playlist_features_list)

             # Parcurgem piesa dupa piesa intreaga lista
        playlist_features = {}

        playlist = self.get_playlist_tracks(self.sp)
        for track in playlist:
            print(track)

            playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
            playlist_features["album"] = track["track"]["album"]["name"]
            playlist_features["track_name"] = track["track"]["name"]
            playlist_features["release_date"] = track["track"]["album"]["release_date"]
            playlist_features["popularity"] = track["track"]["popularity"]
            playlist_features["track_id"] = track["track"]["id"]

            playlist_df["release_date"] = pd.to_datetime(playlist_df["release_date"])
            playlist_df["year"] = pd.DatetimeIndex(playlist_df["release_date"]).year
            playlist_df = playlist_df.drop(columns=['release_date'])
            playlist_df = playlist_df.set_index('track_id')

                 # Preluam proprietatile importante ale melodiilor
            audio_features = self.sp.audio_features(playlist_features["track_id"])[0]
            for feature in playlist_features_list[6:]:
                playlist_features[feature] = audio_features[feature]

                 # Concatenarea tablourilor

            track_df = pd.DataFrame(playlist_features, index=[0])
            playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)
 

        return playlist_df






if __name__ == '__main__':
    playlist = PLAY()
    playlist_datafr = playlist.analiza_playlist(PLAY_CREATE, PLAY_ID)
    convert_to_csv(playlist_datafr)
