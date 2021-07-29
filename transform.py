import json
import pandas as pd
import os

#nos situamos en la direccion de donde queremos llamar los archivos crudos
os.chdir('./data/data_cruda')
archivos = os.listdir()
archivos.sort()

#generamos un bucle por todos los archivos para leerlos, agrupar la información a nivel de municipio contando los casos nuevos. Posteriormente se guarda como csv en el directorio padre del actual.
for archivo in archivos:
    temp_df = pd.read_json(archivo)
    temp_df_agrupado = temp_df.groupby(['fecha_reporte_web','departamento_nom','ciudad_municipio_nom'])['id_de_caso'].count().reset_index()
    temp_df_agrupado.to_csv('../resumen_' + archivo.replace('.json', '.csv'), index=False)