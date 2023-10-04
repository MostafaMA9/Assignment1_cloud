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

def create_targetGroups_method():
    
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
    client = boto3.client('elbv2', region_name="us-east-1")
    
    tg1 = client.create_target_group(
    Name='my-targetGroup1',
    Port=80,
    Protocol='HTTP',
    VpcId=vpc_id,
    )
    print("a new TargetGroup was created")
    # print(tg1)
    tg2 = client.create_target_group(
    Name='my-targetGroup2',
    Port=80,
    Protocol='HTTP',
    VpcId=vpc_id,
    )
    print("a new TargetGroup was created")
    # print(tg2)

    targetGroup_list = []
    targetGroup_list.append(tg1)
    targetGroup_list.append(tg2)
    return targetGroup_list

# in this file we create target groups
if __name__ == '__main__':
    targetGroup_list=create_targetGroups_method()







