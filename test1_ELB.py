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

def hello_elbv2(elbv2_client):
    """
    Use the AWS SDK for Python (Boto3) to create an Elastic Load Balancing V2 client and list
    up to ten of the load balancers for your account.
    This example uses the default settings specified in your shared credentials
    and config files.
    :param elbv2_client: A Boto3 Elastic Load Balancing V2 client object.
    """
    print("Hello, Elastic Load Balancing! Let's list some of your load balancers:")
    load_balancers = elbv2_client.describe_load_balancers(PageSize=10).get('LoadBalancers', [])
    if load_balancers:
        for lb in load_balancers:
            print(f"\t{lb['LoadBalancerName']}: {lb['DNSName']}")
    else:
        print("Your account doesn't have any load balancers.")

def create_load_balancer_method(client):

    response = client.create_load_balancer(
    AvailabilityZones=[
        'us-east-1a',
    ],
    Listeners=[
        {
            'InstancePort': 80,
            'InstanceProtocol': 'HTTP',
            'LoadBalancerPort': 80,
            'Protocol': 'HTTP',
        },
    ],
    LoadBalancerName='my-load-balancer2',
    )

    print(response)
    return response
    



if __name__ == '__main__':
    # elb_client = boto3.client('elbv2', region_name="us-east-1")
    # hello_elbv2(elb_client)
    client = boto3.client('elbv2', region_name="us-east-1")
    my_LB = create_load_balancer_method(client)
    for lb in client.describe_load_balancers()['LoadBalancerDescriptions']:
        print (lb['LoadBalancerName'])
    
    response = client.describe_load_balancers(
    LoadBalancerNames=[
        'my-load-balancer1',
    ],
    )
    print(response)


# ec2 = boto3.client('ec2', region_name="us-east-1" )
# # Retrieves all regions/endpoints that work with EC2
# response = ec2.describe_regions()
# print('Regions:', response['Regions'])
# print("****************")
# # Retrieves availability zones only for region of the ec2 object
# response = ec2.describe_availability_zones()
# print('Availability Zones:', len(response['AvailabilityZones']))
# for ava_zone in response['AvailabilityZones']:
#     print(ava_zone)