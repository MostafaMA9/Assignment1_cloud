import boto3
import time

# Replace these values with your own credentials
aws_access_key_id = ''
aws_secret_access_key = ''
aws_session_token = ''
region_name = 'us-east-1'

# Create a Boto3 session with temporary credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)

# Create an EC2 client
ec2_client = session.client('ec2')

# Define EC2 instance parameters
image_id = 'ami-03a6eaae9938c858c'
instance_type = 't2.micro'
key_name = 'vockey'
security_group_ids = ['sg-04951fe1c296d5fb8']

# Launch the EC2 instance
response = ec2_client.run_instances(
    ImageId=image_id,
    InstanceType=instance_type,
    KeyName=key_name,
    SecurityGroupIds=security_group_ids,
    MaxCount=1,
    MinCount=1
)

# Extract the instance ID
instance_id = response['Instances'][0]['InstanceId']

print(f'Launched EC2 instance with ID: {instance_id}')

delay_seconds = 10
print(f'Terminating EC2 instance {instance_id} in {delay_seconds} seconds...')
time.sleep(delay_seconds)
ec2_client.terminate_instances(InstanceIds=[instance_id])
print(f'Terminated EC2 instance with ID: {instance_id}')
