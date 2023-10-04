# In this file we create functions for load balancer and targeted groups
# In this file we create functions for load balancer and targeted groups
import boto3
from botocore.exceptions import ClientError

def create_target_group(name, protocol, port, vpc_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_target_group(Name=name, Protocol=protocol, Port=port, VpcId=vpc_id)
        print(response)
    except ClientError as e:    
        print(e)


def create_load_balancer(name, security_group_id, subnets, target_group_arns):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_load_balancer(
            Name=name, 
            SecurityGroups=[security_group_id], 
            Subnets=subnets, 
            Scheme='internet-facing', 
            Type='application', 
            IpAddressType='ipv4', 
            Tags=[{'Key': 'Name', 'Value': name}], 
            TargetGroupArn=target_group_arns)
        print(response)
    except ClientError as e:    
        print(e)

def create_listener(load_balancer_arn, protocol, port, target_group_arn):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_listener(
            LoadBalancerArn=load_balancer_arn, 
            Protocol=protocol, 
            Port=port, 
            DefaultActions=[{'Type': 'forward', 'TargetGroupArn': target_group_arn}])
        print(response)
    except ClientError as e:    
        print(e)

def create_rule(listener_arn, field, values, priority, target_group_arn):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_rule(
            ListenerArn=listener_arn,
            Conditions=[
                {
                    'Field': field,
                    'Values': [
                        values,
                    ]
                }
            ],
            Priority=priority,
            Actions=[
                {
                    'Type': 'forward',
                    'TargetGroupArn': target_group_arn,
                },
            ]
        )
        print(response)
    except ClientError as e:
        print(e)