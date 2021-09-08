import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


class Classified:
    def __init__(self):
        dfx = self.dfx
        dfy = self.dfy


    def generate_dataframes(dfx, dfy):

        dfx0 = pd.read_csv("date_X_complet.csv")
        dfx1 = pd.read_csv("date_X_0.csv")
        dfy1 = pd.read_csv("date_y_0.csv")
        dfy0 = pd.read_csv("date_y_complet.csv")
        # concatenam datele colectate recent cu restul setului
        dfx = dfx0.append(dfx1)
        dfy = dfy0.append([dfy1])
        # eliminam duplicatele din set
        dfx = dfx.drop_duplicates(subset=['track_id'])
        dfy = dfy.drop_duplicates(subset=['track_id'])


        print("Marimea tabloului x: {}".format(dfx.shape))
        print("Marimea tabloului y: {}".format(dfy.shape))
        # le salvam inapoi
        dfx.to_csv("date_X_complet.csv",index=False)
        dfy.to_csv("date_y_complet.csv",index=False)

        return dfx, dfy

    def Scaling(self, dfx):
        coloane = dfx.columns
        # facem scalarea de tip minmax
        from sklearn.preprocessing import  MinMaxScaler
        muzica = dfx
        modelScale = MinMaxScaler()
        muzica = pd.DataFrame(modelScale.fit_transform(muzica), index=muzica.index)
        muzica.columns = coloane

        return muzica
    def cluster_PCA(self, muzica):
        # metoda pentru a  aplica PCA spre determinarea coordonatelor fiecarui rand
        muzica = Classified.Scaling(self.dfx)
        pca = PCA().fit(muzica)
        evr = pca.explained_variance_ratio_
        print(evr)
        plt.figure(figsize=(42, 24))
        plt.plot(np.cumsum(pca.explained_variance_ratio_))
        plt.xlabel('number of dimensions')
        plt.ylabel('Explained variance');



    def get_optimal_n_cluster(self, muzica):
        # Testam metoda Kmeans pentru un interval de clustere, si aplicam metoda siluetelor
        range_n_clusters = range(2, 100)
        silhouettes = []
        for n_clusters in range_n_clusters:
            clusterer = KMeans(n_clusters=n_clusters, random_state=10)
            clusterer.fit(muzica)
            cluster_labels = clusterer.predict(muzica)

            silhouette_avg = silhouette_score(muzica, cluster_labels)
            print("For n_clusters =", n_clusters,
                  "The average silhouette_score is :", silhouette_avg)

            silhouettes.append(silhouette_avg)

        for i in range(silhouettes):
            if silhouettes[i] == max(silhouettes):
                n_clusters = i

        return n_clusters
    def KMeans_classifier(self, muzica):
        # Folosind metoda siluetelor, folosind numarul optim de clustere pentru a face clasificarea noastra
        n_clusters = Classified.get_optimal_n_cluster(self.muzica)
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(muzica)
        muzica['type'] = cluster_labels

        muzica.to_csv("muzica_clasificata.csv")
        return muzica



if __name__ == '__main__':

    X,y = Classified.generate_dataframes(X0, y0)



