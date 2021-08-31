from branca.utilities import legend_scaler
from numpy.lib.function_base import quantile

import pandas as pd
import numpy as np
import geopandas as gpd

import requests
import json
import os
from datetime import datetime
from datetime import timedelta
import time
import pickle

import folium

#load the features of each MCPIO

features_ciudad = gpd.read_file('./shp_mapa_municipio/nivel2/MGN_ANM_MPIOCL.dbf')
features_ciudad = features_ciudad[['MPIO_CDPMP', 'STP27_PERS']].groupby('MPIO_CDPMP').sum().reset_index()
features_ciudad.rename(columns={'STP27_PERS':'poblacion'}, inplace=True)

#enrich the summary with the features uploaded before

consolidado = pd.read_csv('./data/consolidado.csv')

cols=['fecha', 'cod_depto','nom_depto','MPIO_CDPMP','nom_mpio','num_casos']
consolidado.columns =cols
consolidado.fecha = pd.to_datetime(consolidado['fecha'], dayfirst=True)
consolidado['MPIO_CDPMP'] = consolidado['MPIO_CDPMP'].apply(lambda x: '0' * (5-len(str(x)))+str(x))

consolidado = consolidado.merge(features_ciudad, on='MPIO_CDPMP', how='left')
consolidado['cod_depto'] = consolidado['MPIO_CDPMP'].str[:2]

consolidado['casos_por_millon'] = np.ceil(consolidado['num_casos'] / (consolidado['poblacion'] /1000000))

df_ultimo = consolidado[consolidado['fecha']==max(consolidado['fecha'])]

#create the dictionary for filters, dropdown and others objects

depto_dict = {}
mpio_dict = {}

for depto in consolidado['cod_depto'].unique():
    
    temp = consolidado[consolidado['cod_depto']==depto]
    depto_dict[temp['nom_depto'].unique()[0]] = depto
    mpio_dict[depto] = {i['nom_mpio']:i['MPIO_CDPMP'] for i in temp[['MPIO_CDPMP','nom_mpio']].to_dict('records')}


#create the map for MPIO using the enrich dataset

mapa_municipios = gpd.read_file('./shp_mapa_municipio/MGN_MPIO_POLITICO.shp')
mapa_municipios = mapa_municipios[mapa_municipios['MPIO_CDPMP'].isin(df_ultimo['MPIO_CDPMP'].unique())]
mapa_municipios = mapa_municipios.merge(how='left', right=df_ultimo[['MPIO_CDPMP','casos_por_millon']], on='MPIO_CDPMP')

mapa = folium.Map(location=[4.3, -73.40], tiles='cartodbpositron', zoom_start=5.5, min_zoom=6, max_zoom=7)

bins = list(df_ultimo['casos_por_millon'].quantile([0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1]))

capa = folium.Choropleth(
    geo_data=mapa_municipios, 
    name="Casos por millon - Municipio", 
    data=df_ultimo,
    columns=['MPIO_CDPMP', 'casos_por_millon'],
    key_on='feature.properties.MPIO_CDPMP',
    smooth_factor=0,
    fill_color='OrRd',
    bins=bins
    )

capa.add_to(mapa)
capa.geojson.add_child(folium.features.GeoJsonTooltip(['MPIO_CNMBR', 'casos_por_millon'], labels=False))
folium.LayerControl().add_to(mapa)





#export all the assets created before
mapa.save('./assets/mapa_resumen.html')

consolidado.to_csv('./assets/historico.csv', index=False)
df_ultimo.to_csv('./assets/ultimo.csv', index=False)

with open('./assets/depto_dict.pkl', 'wb') as fp:
    pickle.dump(depto_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)

with open('./assets/mpio_dict.pkl', 'wb') as fp:
    pickle.dump(mpio_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)