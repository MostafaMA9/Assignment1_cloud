import boto3
from botocore.exceptions import ClientError

def create_key_pair(ec2, key_name):
    try:
        response = ec2.create_key_pair(KeyName=key_name)
        return response
    except ClientError as e:
        print(e)

def delete_key_pair(ec2, key_name):
    try:
        response = ec2.delete_key_pair(KeyName=key_name)
        return response
    except ClientError as e:
        print(e)