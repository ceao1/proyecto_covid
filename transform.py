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
    temp_df_agrupado = temp_df.groupby(['fecha_reporte_web','departamento','departamento_nom','ciudad_municipio','ciudad_municipio_nom'])['id_de_caso'].count().reset_index()
    os.chdir('../')
    temp_df_agrupado.to_csv('./data_resumida/resumen_' + archivo.replace('.json', '.csv'), index=False)
    #guardo el ultimo archivo para tenerlo de referencia en los formatos y columnas por si se necesita cambiar la agrupacion mas adelante
    os.chdir('./data_cruda')
    os.remove(archivo)

os.chdir('..')
os.chdir('./data_resumida')
resumenes = os.listdir()
resumenes.sort()
os.chdir('..')
for resumen in resumenes:
    
    with open('./data_resumida/'+resumen, 'r') as fuente, open('consolidado.csv', 'a') as consolidado:
        contador = 0
        for line in fuente:
            contador = contador + 1
            if contador == 1:
                continue
            else:
                consolidado.write(line)
    os.remove('./data_resumida/'+resumen)