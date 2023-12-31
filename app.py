import subprocess
import boto3
import os
from dotenv import load_dotenv
import requests
import threading
from datetime import datetime
import time
from instances import *
from KeyPair import *
from SecurityGroup import *
from ELB import *
from benchmark import *
from analysis import *

# Install required Python packages
subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

# Load AWS credentials from credentials.env
load_dotenv("credentials.env")
aws_access_key_id = os.environ["aws_access_key_id"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
aws_session_token = os.environ["aws_session_token"]

# Define EC2 instance parameters
keyPairName = 'LOG8415E'
securityGroupName = 'LOG8415E_B2'

# Create an EC2 client
EC2 = boto3.client(
    'ec2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

# create elastic load balancer

ELBV2 = boto3.client(
    'elbv2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

# Cloudwatch client
CW = boto3.client(
    'cloudwatch',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

# get vpc_id
vpc_id = EC2.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
subnet1 = EC2.describe_subnets().get('Subnets', [{}])[0].get('SubnetId', '')
subnet2 = EC2.describe_subnets().get('Subnets', [{}])[1].get('SubnetId', '')

# create key pair and security group
print('Creating key pair...')
create_key_pair(EC2, keyPairName)
print('Creating security group...')
security_group = create_security_group(EC2, securityGroupName, vpc_id)

# Create 4 m4.large instances
m4Large_cluster_ids = create_m4large_instances(EC2, keyPairName, security_group['GroupId'], subnet1)
print('Cluster 1 ids: ')
print(m4Large_cluster_ids)

# Create 4 t2.large instances
t2Large_cluster_ids = create_t2large_instances(EC2, keyPairName, security_group['GroupId'], subnet2)
print('Cluster 2 ids: ')
print(t2Large_cluster_ids)

# Wait for instances to initialise
print("Waiting 4 minute for instances to initialise")
time.sleep(240)

print('Creating load balancer...')
load_balancer = create_load_balancer(ELBV2, 'load-balancer', security_group['GroupId'], [subnet1, subnet2])
elb_dns = str(load_balancer.get('LoadBalancers')[0].get('DNSName'))
print("ELB was created. DNS: " + elb_dns)

print('Creating target groups...')
target_group1 = create_target_group(ELBV2, 'target-group1', 'HTTP', 80, vpc_id)
target_group2 = create_target_group(ELBV2, 'target-group2', 'HTTP', 80, vpc_id)

print('Creating listener...')
listener = create_listener(ELBV2, load_balancer['LoadBalancers'][0]['LoadBalancerArn'], 'HTTP', 80, target_group1['TargetGroups'][0]['TargetGroupArn'], target_group2['TargetGroups'][0]['TargetGroupArn'])

print('Creating rules...')
rule1 = create_rule(ELBV2, listener['Listeners'][0]['ListenerArn'], 'path-pattern', '/cluster1', 1,
                    target_group1['TargetGroups'][0]['TargetGroupArn'])
rule2 = create_rule(ELBV2, listener['Listeners'][0]['ListenerArn'], 'path-pattern', '/cluster2', 2,
                    target_group2['TargetGroups'][0]['TargetGroupArn'])

# Register 5 m4.large instances to target group 1 and 4 t2.large instances to target group 2
register_instances_to_target_groups(ELBV2, m4Large_cluster_ids, t2Large_cluster_ids, target_group1, target_group2)

print("Waiting 2 minutes for ELB to get activated")
time.sleep(120)

print("Waiting 1 minutes for target groups to be healthy")
time.sleep(60)
print('Done')

# Benchmark
benchmark(elb_dns)

print("Waiting 1 minute before running the analysis...")
time.sleep(60)

# cloudwatch metrics analysis
print("Running analysis...")
analysis(CW, m4Large_cluster_ids, t2Large_cluster_ids, target_group1, target_group2)

print("Deleting the load balancer (in the same time deleting the listener and rules)...")
time.sleep(30)

print('Deleting rules...')
delete_rule(ELBV2, rule1['Rules'][0]['RuleArn'])
delete_rule(ELBV2, rule2['Rules'][0]['RuleArn'])
time.sleep(10)

print('Deleting listener...')
delete_listener(ELBV2, listener['Listeners'][0]['ListenerArn'])
time.sleep(10)

# unregister the instances
unregister_instances_from_target_groups(ELBV2, m4Large_cluster_ids, t2Large_cluster_ids, target_group1, target_group2)
time.sleep(10)

print('Deleting load balancer...')
delete_load_balancer(ELBV2, load_balancer['LoadBalancers'][0]['LoadBalancerArn'])
time.sleep(10)

print('Deleting target groups...')
delete_target_group(ELBV2, target_group1['TargetGroups'][0]['TargetGroupArn'])
delete_target_group(ELBV2, target_group2['TargetGroups'][0]['TargetGroupArn'])
time.sleep(10)

print("Terminating instances...")
terminate_instance(EC2, m4Large_cluster_ids)
terminate_instance(EC2, t2Large_cluster_ids)

print("Waiting 1 minute to make sure all instances are terminated ")
time.sleep(60)

print('Deleting security group...')
delete_security_group(EC2, securityGroupName)
time.sleep(10)

print('Deleting key pair...')
delete_key_pair(EC2, keyPairName)
print('Done')
