import boto3
region = 'us-east-1' #whatever region you have your instances
instances = ['i-0d2cdb18e3XXXXXXX', 'i-0443fb963bXXXXX'] #the isntance id of ec2 instances
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.start_instances(InstanceIds=instances)
    print('Started your instances: ' + str(instances))