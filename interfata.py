# reprezentarile grafice ale datelor noastre

import dash
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
from scipy.cluster.hierarchy import dendrogram, linkage
import plotly.express as px

from dash import html, dcc
from dash.dependencies import Input, Output
from scipy.spatial.distance import pdist, squareform

app = dash.Dash(__name__)

# Importam cele 2 seturi de date(playlist + coordonatele fiecarei melodii)
df1 = pd.read_csv('coord_3.csv',encoding="ISO-8859-1")
df2 = pd.read_csv('dataset_complete.csv',encoding="ISO-8859-1")
df3 = pd.read_csv('cluster_points.csv',encoding="ISO-8859-1")
df2['maintype'] = df3['cluster']
# preluam proprietatile uzuale pentru fiecare melodie din playlist
copie = df2.drop(columns=['track_id', 'artist', 'album', 'track_name', 'type', 'maintype', 'cluster', 'shortest_distance_to_point', 'closest_neighbour'])
X = copie.drop(columns=['key', 'mode', 'time_signature', 'year', 'tempo', 'duration_ms'])

# Primul grafic - separarea pieselor in clustere si distantele dintre acestea
df1['maintype'] = df3['cluster']
df1['distance'] = df2['shortest_distance_to_point']
df1['label'] = df2['artist']

fig = px.scatter_3d(df1, x='0', y='1', z='2', color='maintype', size_max=20, title="Separarea melodiilor pe clustere" )
fig.show()

# heatmap cu toate proprietatile uzuale ale melodiilor(acusticitate, zgomot, energie, dansabilitate, valenta, rata de vorbire in piesa, cat de instrumentala e piesa)

'''

app.layout = html.Div([
    html.P("Relatia dintre proprietatile:"),
    dcc.Checklist(
        id='medals',
        options=[{'label': x, 'value': x}
                 for x in X.columns],
        value=X.columns.tolist(),
    ),
    dcc.Graph(id="graph"),
])
fig2 = px.imshow(X[cols])


graphRow1 = dbc.Row([dbc.Col(fig,md=12)])
graphRow2 = dbc.Row([dbc.Col(fig2, md=6)])
'''
if __name__ == '__main__':
    app.run_server(debug=True)

