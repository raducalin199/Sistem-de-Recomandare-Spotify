import pandas as pd
from scipy.spatial import distance
import random

info = pd.read_csv("dataset_complete.csv")
info_y = info.filter(items=['track_id', 'artist', 'album', 'track_name', 'year', 'maintype', 'type', 'cluster','shortest_distance_to_point','closest_neighbour'])
info_x = info.drop(columns=['track_id', 'artist', 'album', 'track_name', 'year', 'maintype', 'type', 'cluster','shortest_distance_to_point','closest_neighbour'])
coloane = info_y.columns
N_PIESE_PLAYLIST = 50

def generate_dataframe(y, playlist_df, track_df):
    playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)
    y = y.drop(track_df.index)
    return playlist_df


class playlist:
    def __init__(self, X, y = info_y ):
        self.y = y
        self.X = X


    def row_dropping_tracks(self, X, y):
        '''

        functia este folosita pentru a elimina toate piesele din lista y care coincid cu piesele din lista X
        '''
        for i in range(y):
            if y.loc[i,"track_id"] == X.values[:,0]:
                y = y.drop(i)
        return self.y

    def playlist_creator_random_songs(self, X, y):
        '''

        :param X: dintr-un calup de melodii din playlist se vor alege alte melodii similare intr-un mod aleatoriu
        :param y:
        :return: playlistul cu piese similare
        '''
        y = self.row_dropping_tracks(self.X, self.y)
        playlist_df = pd.DataFrame(columns=coloane)
        clasa = 250
        lung = len(y.loc[y['cluster'] == clasa])
        i = 0
        n_tracks = 100

        while (i < n_tracks):
            track_df = y.sample()
            x = X.sample()
            lung = len(y.loc[y['cluster'] == clasa])
            if ((track_df.values[:, 7] == clasa) and (track_df.values[:, 3] != x.values[:,3])):
                playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)
                y = y.drop(track_df.index)
                i += 1
                if (i == 100):
                    break
                if (len(y.loc[y['cluster'] == clasa]) - 1 == 0):
                    row_clasa = y[y.maintype.values == x.values[:,3]].iloc[0]
                    clasa = row_clasa[7]
            elif (track_df.values[:, 7] != clasa) and (track_df.values[:, 1] == X.values[:, 1]):
                clasa = track_df.values[:, 7]
                playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)
                y = y.drop(track_df.index)
                i += 1
                if (i == 100):
                    break
                if (len(y.loc[y['clasa'] == clasa]) - 1 == 0):
                    row_clasa = y[y.maintype.values == x.values[:, 3]].iloc[0]
                    clasa = row_clasa[7]
        return playlist_df

    def playlist_creator_one_song(self, X):
        '''

        :param X: o piesa selectata la nimereala de la care se va porni playlistul
        :return: playlistul cu melodii similare cu X
        '''
        y = self.row_dropping_tracks(self.X, self.y)
        playlist_df = pd.DataFrame(columns=coloane)
        clasa = X[4]
        lung = len(y.loc[y['class'] == clasa])
        i = 0
        n_tracks = N_PIESE_PLAYLIST

        while (i < n_tracks):
            track_df = y.sample()
            if (track_df.values[:, 4] == clasa) and (track_df.values[:, 3] !=X.values[:,3]):
                playlist_df = generate_dataframe(y, playlist_df, track_df)
                i += 1
                print(i)
                if i == 100:
                    break
                if (len(y.loc[y['clasa'] == clasa]) - 1) == 0:
                    row_clasa = y[y.maintype.values == X.values[:, 3]].iloc[0]
                    clasa = row_clasa[7]
            elif(track_df.values[:, 7] != clasa) and (track_df.values[:, 1] !=X.values[:,1]):
                clasa = track_df.values[:, 7]
                clasa = track_df.values[:, 7]
                playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)
                y = y.drop(track_df.index)
                i += 1
                if (i == 100):
                    break
                if (len(y.loc[y['clasa'] == clasa]) - 1 == 0):
                    row_clasa = y[y.maintype.values == X.values[:, 3]].iloc[0]
                    clasa = row_clasa[7]

        return playlist_df


    def propunere_noua(self, X, y):
        '''
        In comparatie cu celelalte 2 metode care folosesc valoarea clusterului din care fac parte,
         in cazul de fata folosim distanta minima dintre puncte pentru a determina playlistul dorit

        '''
        y = self.row_dropping_tracks(self.X, self.y)
        playlist_df = pd.DataFrame(columns=coloane)
        i = 0
        n_tracks = N_PIESE_PLAYLIST
        Xd = X[X.shortest_distance_to_point == min(X.values[:, 9])].iloc[0]

        while (i < n_tracks):
            track_df = y.sample()
            if (track_df.index <= Xd[9]):
                playlist_df = generate_dataframe(y, playlist_df, track_df)
                i += 1
                print(i)
                if i == 100:
                    break


        return playlist_df


