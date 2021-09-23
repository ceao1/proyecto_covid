import requests
import json
from datetime import datetime
from datetime import timedelta
import boto3

def lambda_handler(event, context):
    # TODO implement
    ayer = datetime.today() + timedelta(days=-1)

    fecha = str(ayer.day) + '/' + str(ayer.month) + '/' + str(ayer.year) + ' 0:00:00'
    resultado = requests.get("https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100000&$where=(fecha_reporte_web="+"'"+fecha+"')")
    
    str_archivo = str(ayer.date()).replace('-', '') + '.json'
    
    client = boto3.client('s3')
    client.put_object(Body=json.dumps(resultado.json()), Bucket='your_bucket', Key=str_archivo)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Se cargo existosamente el archivo: '+ str_archivo),
        'hour': datetime.now().strftime('%d-%B-%y %H-%M')
    }
