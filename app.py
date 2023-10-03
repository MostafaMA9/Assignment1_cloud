import subprocess
subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
import boto3
import os
from dotenv import load_dotenv
from time import time

from instances import *
from KeyPair import *
from SecurityGroup import *

load_dotenv("./credentials")
aws_access_key_id = os.environ["aws_access_key_id"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
aws_session_token = os.environ["aws_session_token"]

# Define EC2 instance parameters
keyPairName = 'LOG8415E'
securityGroupName = 'LOG8415E_LAB_B1'


# Create an EC2 client
EC2 = boto3.client(
    'ec2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)


#get vpc_id
vpc_id = EC2.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')

#create key pair and security group
print('Creating key pair...')
create_key_pair(EC2, keyPairName)
print('Creating security group...')
create_security_group(EC2, securityGroupName, vpc_id)

#Create 5 m4.large instances
m4Large_cluster_ids = create_m4large_instances(EC2, keyPairName, securityGroupName)

#Create 4 t2.large instances
t2Large_cluster_ids = create_t2large_instances(EC2, keyPairName, securityGroupName)


#terminating instances
