import pandas as pd
import requests
import requests
import json
from datetime import datetime
from datetime import timedelta

ayer = datetime.today() + timedelta(days=-1)
otro_dia = ayer + timedelta(days=-1)


#convierto la fecha de hoy en el formato que lo acepta la consulta de api
fecha = str(ayer.day) + '/' + str(ayer.month) + '/' + str(ayer.year) + ' 0:00:00'
#fecha = str(otro_dia.day) + '/' + str(otro_dia.month) + '/' + str(otro_dia.year) + ' 0:00:00'


#se realiza la peticion al api para traer los datos de la fecha de hoy
resultado = requests.get("https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100000&$where=(fecha_reporte_web="+"'"+fecha+"')")


#se crea una variable con el nombre con el que se guardaran los datos, en formato json
nombre_archivo = str(ayer.date()).replace('-', '') + '.json'
#nombre_archivo = str(otro_dia.date()).replace('-', '') + '.json'


#se crea la ruta para guardar el archivo
ruta_archivo = './data/data_cruda/' + nombre_archivo

#se crea el archivo con el nombre asociado al día descargado
with open(ruta_archivo, 'w') as fp:
    json.dump(resultado.json(), fp)
    