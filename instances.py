# Here we create our instances. First function is for creating M4.large instances and the second one is for creating t2.large instances
import boto3
from botocore.exceptions import ClientError

def create_instances(number, image_id, instance_type, security_group_id, key_name):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.run_instances(ImageId=image_id, InstanceType=instance_type, MinCount=1, MaxCount=number, SecurityGroupIds=[security_group_id], KeyName=key_name)
        print(response)
    except ClientError as e:
        print(e)