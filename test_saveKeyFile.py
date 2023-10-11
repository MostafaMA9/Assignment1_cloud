import boto3
import os
from dotenv import load_dotenv
from time import time

from ELB import *
from SecurityGroup import *
from KeyPair import *

load_dotenv("./credentials")
aws_access_key_id = os.environ["aws_access_key_id"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
aws_session_token = os.environ["aws_session_token"]

# Define EC2 instance parameters
keyPairName = 'key_test001'


# Create an EC2 client
EC2 = boto3.client(
    'ec2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)


ELBV2 = boto3.client(
    'elbv2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

 




def create_key_pair1(ec2, key_name):
    try:
        response = ec2.create_key_pair(KeyName=key_name)
        private_key = response["KeyMaterial"]
        with os.fdopen(os.open(os.getcwd().replace("\\","/")+"/"+key_name+".pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)
        return response 
    except ClientError as e:
        print(e)



create_key_pair1(EC2, keyPairName)