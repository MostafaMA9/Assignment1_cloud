# In this file we create functions for load balancer and targeted groups
# In this file we create functions for load balancer and targeted groups
import boto3
from botocore.exceptions import ClientError

def create_target_group(client, name, protocol, port, vpc_id):
    try:
        response = client.create_target_group(Name=name, Protocol=protocol, Port=port, VpcId=vpc_id)
        return response
    except ClientError as e:    
        print(e)


def create_load_balancer(client, name, security_group_id, subnets, target_group_arns):
    try:
        response = client.create_load_balancer(
            Name=name, 
            SecurityGroups=[security_group_id], 
            Subnets=subnets, 
            Scheme='internet-facing', 
            Type='application', 
            IpAddressType='ipv4', 
            Tags=[{'Key': 'Name', 'Value': name}], 
            TargetGroupArn=target_group_arns)
        return response
    except ClientError as e:    
        print(e)

def create_listener(client, load_balancer_arn, protocol, port, target_group_arn):
    try:
        response = client.create_listener(
            LoadBalancerArn=load_balancer_arn, 
            Protocol=protocol, 
            Port=port, 
            DefaultActions=[{'Type': 'forward', 'TargetGroupArn': target_group_arn}])
        return response
    except ClientError as e:    
        print(e)

def create_rule(client, listener_arn, field, values, priority, target_group_arn):
    try:
        response = client.create_rule(
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