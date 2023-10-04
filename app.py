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
subnet1 = EC2.describe_subnets().get('Subnets', [{}])[0].get('SubnetId', '')
subnet2 = EC2.describe_subnets().get('Subnets', [{}])[1].get('SubnetId', '')

ELBV2 = boto3.client(
    'elbv2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

 
#create key pair and security group
print('Creating key pair...')
key_pair = create_key_pair(EC2, keyPairName)
print('Creating security group...')
security_group = create_security_group(EC2, securityGroupName, 'LOG8415E_LAB_B1', vpc_id)
print('Creating target groups...')
target_group1 = create_target_group(ELBV2,'target-group1', 'HTTP', 80, vpc_id)
target_group2 = create_target_group(ELBV2,'target-group2', 'HTTP', 80, vpc_id)
print('Creating load balancer...')
load_balancer = create_load_balancer(ELBV2,'load-balancer', security_group['GroupId'], [subnet1,subnet2])
print('Creating listener...')
listener = create_listener(ELBV2, load_balancer['LoadBalancers'][0]['LoadBalancerArn'], 'HTTP', 80, target_group1['TargetGroups'][0]['TargetGroupArn'])
print('Creating rules...')
rule1 = create_rule(ELBV2,listener['Listeners'][0]['ListenerArn'], 'path-pattern', '/cluster1', 1, target_group1['TargetGroups'][0]['TargetGroupArn'])
rule2 = create_rule(ELBV2,listener['Listeners'][0]['ListenerArn'], 'path-pattern', '/cluster2', 2, target_group2['TargetGroups'][0]['TargetGroupArn'])
print('Done')
print('Deleting rules...')
delete_rule(ELBV2,rule1['Rules'][0]['RuleArn'])
delete_rule(ELBV2,rule2['Rules'][0]['RuleArn'])
print('Deleting listener...')
delete_listener(ELBV2,listener['Listeners'][0]['ListenerArn'])
print('Deleting load balancer...')
delete_load_balancer(ELBV2,load_balancer['LoadBalancers'][0]['LoadBalancerArn'])
print('Deleting target groups...')
delete_target_group(ELBV2,target_group1['TargetGroups'][0]['TargetGroupArn'])
delete_target_group(ELBV2,target_group2['TargetGroups'][0]['TargetGroupArn'])
print('Deleting security group...')
delete_security_group(EC2, security_group['GroupId'])
print('Deleting key pair...')
delete_key_pair(EC2, keyPairName)
print('Done')