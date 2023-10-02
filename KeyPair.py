import boto3
from botocore.exceptions import ClientError

def create_key_pair(key_name):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_key_pair(KeyName=key_name)
        print(response)
    except ClientError as e:
        print(e)