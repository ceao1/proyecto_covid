import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


import pandas as pd
import numpy as np
import geopandas as gpd
import folium
import pickle
from datetime import datetime
import locale 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

'''
~~ insumos
'''
locale.setlocale(locale.LC_TIME, 'es_CO.utf8') 

depto_dict={}

mpio_dict={}

df_ultimo=pd.read_csv('./assets/ultimo.csv')

df_historico=pd.read_csv('./assets/historico.csv')

casos_ultimo = df_ultimo['num_casos'].sum()
ultima_fecha = df_ultimo['fecha'].iloc[0]
ultima_fecha = datetime.strptime(ultima_fecha, '%Y-%m-%d').date()
ultima_fecha = ultima_fecha.strftime('%d de %B', )
'''
~~~~~~~~~~~~~~~~
~~ APP LAYOUT ~~
~~~~~~~~~~~~~~~~
'''


app.layout = html.Div(children=[

    html.Div([
        html.H1('Reporte de COVID - Carlos Anzola', className='app-header')
    ]),

    html.Div([
        html.Div([
            html.H5('El total de casos del {fecha} fue: {casos}'.format(fecha= ultima_fecha, casos= casos_ultimo)),
           
        ]),
        html.Br(),

        html.Div([
            html.Iframe(src='./assets/mapa_resumen.html', className='six columns', style={'height':'700px'}),
            dcc.Graph(className='six columns', style={'padding-top':'50px'})




        ])
    ])
])





if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)