# In this file we create functions for load balancer and targeted groups
import boto3
from botocore.exceptions import ClientError

def create_target_group(ec2, name, protocol, port, vpc_id):
    try:
        response = ec2.create_target_group(Name=name, Protocol=protocol, Port=port, VpcId=vpc_id)
        return response
    except ClientError as e:    
        print(e)


def create_load_balancer(ec2, name, security_group_id, subnets):
    try:
        response = ec2.create_load_balancer(
            Name=name, 
            SecurityGroups=[security_group_id], 
            Subnets=subnets, 
            Scheme='internet-facing', 
            Type='application', 
            IpAddressType='ipv4', 
            Tags=[{'Key': 'Name', 'Value': name}], )
        return response
    except ClientError as e:    
        print(e)

def create_listener(ec2, load_balancer_arn, protocol, port, target_group_arn):
    try:
        response = ec2.create_listener(
            LoadBalancerArn=load_balancer_arn, 
            Protocol=protocol, 
            Port=port, 
            DefaultActions=[{'Type': 'forward', 'TargetGroupArn': target_group_arn}])
        return response
    except ClientError as e:    
        print(e)

def create_rule(ec2, listener_arn, field, values, priority, target_group_arn):
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
        return response
    except ClientError as e:
        print(e)

def delete_target_group(ec2, target_group_arn):
    try:
        response = ec2.delete_target_group(TargetGroupArn=target_group_arn)
        return response
    except ClientError as e:
        print(e)

def delete_load_balancer(ec2, load_balancer_arn):
    try:
        response = ec2.delete_load_balancer(LoadBalancerArn=load_balancer_arn)
        return response
    except ClientError as e:
        print(e)

def delete_listener(ec2, listener_arn):
    try:
        response = ec2.delete_listener(ListenerArn=listener_arn)
        return response
    except ClientError as e:
        print(e)

def delete_rule(ec2, rule_arn):
    try:
        response = ec2.delete_rule(RuleArn=rule_arn)
        return response
    except ClientError as e:
        print(e)