import pandas as pd
import secret_data
import spotipy
import spotipy.util as util
import playlist_generator_one_user
import classifier


def convert_to_csv(playlist_df):
    playlist_df.drop(
        columns=["track_id","artist", "album", "track_name", "release_date",]).to_csv(
        "date_X_0.csv")
    playlist_df.filter(['artist', 'album', 'track_name']).to_csv("date_y_0.csv")

class PLAY:
    def __init__(self, client_id = secret_data.CLIENT_ID, client_secret=secret_data.CLIENT_SECRET):
        '''
        Prin functia de initializare a datelor se face si autentificarea catre Spotify API
        '''

        self.client_id = client_id
        self.client_secret = client_secret

        token = util.spotipy.oauth2.SpotifyClientCredentials(client_id=self.client_id,
                                                              client_secret=self.client_secret)
        cache_token = token.get_access_token(as_dict=False)
        self.sp = spotipy.Spotify(cache_token)


    def get_playlist_tracks(self, sp):
        '''
            Functie care preia rand pe rand toate piesele ce alcatuiesc un playlist curent
        '''
        results = self.sp.user_playlist_tracks(self.creator, self.playlist_id)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        return tracks


    def get_user_tracks(self):
       # preluam toate melodiile
        offset = 0
        songs = []
        while True:
            melody = self.sp.current_user_saved_tracks(limit=50, offset=offset)
            songs += melody['items']
            if melody['next'] is not None:
                offset += 100
            else:
                break

        liked_df = self.scatter_tracks(songs)
        return liked_df



    def scatter_tracks(self, songs):
        playlist_features_list = ["artist", "album", "track_name", "release_date", "track_id", "acousticness"
                                  "danceability", "energy",
                                  "key", "loudness", "mode", "speechiness",
                                  "instrumentalness", "liveness", "valence", "tempo", "duration_ms",
                                  "time_signature"]
        playlist_features = {}
        playlist_df = pd.DataFrame(columns=playlist_features_list)
        for track in songs:
            # Mai intai incepem sa preluam informatiile meta
            playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
            playlist_features["album"] = track["track"]["album"]["name"]
            playlist_features["track_name"] = track["track"]["name"]
            playlist_features["release_date"] = track["track"]["album"]["release_date"]
            playlist_features["track_id"] = track["track"]["id"]

            # Preluam proprietatile importante ale melodiilor
            audio_features = self.sp.audio_features(playlist_features["track_id"])[0]
            for feature in playlist_features_list[5:]:
                playlist_features[feature] = audio_features[feature]

                # Concatenarea tablourilor

            track_df = pd.DataFrame(playlist_features, index=[0])
            playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)

        playlist_df["release_date"] = pd.to_datetime(playlist_df["release_date"])
        playlist_df["year"] = pd.DatetimeIndex(playlist_df["release_date"]).year
        playlist_df = playlist_df.drop(columns=['release_date'])
        return  playlist_df

    def analiza_playlist( self, creator,  playlist_id):
        '''

        :param creator: Utilizatorul care a compus playlistul
        :param playlist_id: Cod de identificare al playlistului(public)
        :return: Prin intermediul Spotipy, se vor extrage rand pe rand piesele din playlist folosind metoda precedenta
        si le va concatena intr-un dataframe dedicat playlistului
        '''

        playlist = self.get_playlist_tracks(self.sp)

        playlist_df = self.scatter_tracks(playlist)
        return playlist_df


    def create_spotify_playlist(self,sp):
      playlist =  playlist_generator_one_user.playlist(X=self.get_user_tracks(), y=self.analiza_playlist())

      plyst = self.sp.user_playlist_create(username=secret_data.PLAY_CREATE,
                                          name="Playlist_cu_cluster :)")
      df_Z = playlist.playlist_creator_random_songs(playlist.X, playlist.y)
      self.sp.user_playlist_add_tracks(user=df_Z[:,3],
                                playlist_id=plyst['id'],
                                tracks=df_Z[:,0])


# In main se vor apela toate metodele, inclusiv cele ce tin de melodie
if __name__ == '__main__':
    clasificator = classifier.Classified()
    # Extragerea unui playlist fixat de pe Spotify
    q = input("Alegeti intre extragerea pieselor din playlist public sau playlist personal(Liked Tracks): ")
    if (q == '1'):
        playlist = PLAY()
        playlist_datafr = playlist.analiza_playlist(secret_data.PLAY_CREATE, secret_data.PLAY_ID)
        convert_to_csv(playlist_datafr)
    else:
        preferate = PLAY()
        preferate.create_spotify_playlist(preferate.sp)


