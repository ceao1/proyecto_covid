import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
import os

for i in range(-1, 0):
    ayer = datetime.today() + timedelta(days=i)
    fecha = str(ayer.day) + '/' + str(ayer.month) + '/' + str(ayer.year) + ' 0:00:00'


    resultado = requests.get("https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100000&$where=(fecha_reporte_web="+"'"+fecha+"')")
    if len(resultado.json()) == 0:
        pass
    else:
        
        df = pd.DataFrame.from_records(resultado.json())


        columnas = ['ciudad_municipio',
        'ciudad_municipio_nom',
        'departamento',
        'departamento_nom',
        'edad',
        'estado',
        'fecha_de_notificaci_n',
        'fecha_diagnostico',
        'fecha_inicio_sintomas',
        'fecha_muerte',
        'fecha_recuperado',
        'fecha_reporte_web',
        'fuente_tipo_contagio',
        'id_de_caso',
        'nom_grupo_',
        'pais_viajo_1_cod',
        'pais_viajo_1_nom',
        'per_etn_',
        'recuperado',
        'sexo',
        'tipo_recuperacion',
        'ubicacion',
        'unidad_medida']


        for col in columnas:
            if col == columnas[0]:
                final = df[[col]]
            else:
                try:
                    final = pd.concat([final, df[[col]]], axis=1)
                except:
                    final = pd.concat([final, pd.Series(name=col)], axis=1)




        col_int = ['ciudad_municipio', 
        'departamento',
        'edad',
        'id_de_caso',
        'pais_viajo_1_cod',
        'per_etn_',
        'unidad_medida']

        for col in col_int:
            try:
                final[col] = final[col].astype(int)
            except:
                pass


        col_dates = ['fecha_de_notificaci_n',
        'fecha_diagnostico',
        'fecha_inicio_sintomas',
        'fecha_muerte',
        'fecha_recuperado',
        'fecha_reporte_web']

        for col in col_dates:
            final[col] = pd.to_datetime(final[col], dayfirst=True)
        
        final.to_csv('cargar.csv', index=False)
        text_os = "PGPASSWORD='$PASSWORD' psql -h your_database.XXXXXXXgp3ln.us-east-1.rds.amazonaws.com -U user -d covid_db -c '\copy covid from '~/Documents/proyecto_covid/cargar.csv' with (format csv, header true);'" #be careful with the path to file
        os.system(text_os)