import pandas as pd
import requests
import requests
import json
from datetime import datetime
from datetime import timedelta

hoy = datetime.today()
otro_dia = hoy + timedelta(days=-5)


#convierto la fecha de hoy en el formato que lo acepta la consulta de api
fecha = str(hoy.day) + '/' + str(hoy.month) + '/' + str(hoy.year) + ' 0:00:00'
#fecha = str(otro_dia.day) + '/' + str(otro_dia.month) + '/' + str(otro_dia.year) + ' 0:00:00'


#se realiza la peticion al api para traer los datos de la fecha de hoy
resultado = requests.get("https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100000&$where=(fecha_reporte_web="+"'"+fecha+"')")


#se crea una variable con el nombre con el que se guardaran los datos, en formato json
nombre_archivo = str(hoy.date()).replace('-', '') + '.json'
#nombre_archivo = str(otro_dia.date()).replace('-', '') + '.json'


#se crea la ruta para guardar el archivo
ruta_archivo = './data/' + nombre_archivo

with open(ruta_archivo, 'w') as fp:
    json.dump(resultado.json(), fp)


