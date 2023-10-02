# Here we create our instances. First function is for creating M4.large instances and the second one is for creating t2.large instances
import boto3
from botocore.exceptions import ClientError

def create_instances(image_id, instance_type, number, subnet_id, security_group_id, key_name):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.run_instances(
            ImageId=image_id, 
            InstanceType=instance_type, 
            Count=number,
            SubnetId=subnet_id,
            SecurityGroupIds=[security_group_id], 
            KeyName=key_name)
        print(response)
    except ClientError as e:
        print(e)

def create_vpc(id, cidr_block):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_vpc(Id=id,CidrBlock=cidr_block)
        print(response)
    except ClientError as e:
        print(e)

def create_subnet(id, cidr_block, vpc_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_subnet(
            Id=id,
            CidrBlock=cidr_block,
            VpcId=vpc_id)
        print(response)
    except ClientError as e:
        print(e)