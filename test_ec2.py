import boto3
import time

# Replace these values with your own credentials and configuration
aws_access_key_id = 'YOUR_ACCESS_KEY'
aws_secret_access_key = 'YOUR_SECRET_KEY'
aws_session_token = 'YOUR_SESSION_TOKEN'
region_name = 'us-east-1'
image_id = 'ami-03a6eaae9938c858c'
instance_type = 't2.micro'
key_name = 'YOUR_KEY_PAIR_NAME'
security_group_ids = ['sg-04951fe1c296d5fb8']
delay_seconds = 10

# Create a Boto3 session with credentials and region
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)

# Create an EC2 client
ec2_client = session.client('ec2')

def launch_ec2_instance():
    try:
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
        return instance_id

    except Exception as e:
        print(f"An error occurred during instance launch: {str(e)}")
        return None

def terminate_ec2_instance(instance_id):
    if instance_id:
        try:
            # Wait for the specified delay
            print(f'Terminating EC2 instance {instance_id} in {delay_seconds} seconds...')
            time.sleep(delay_seconds)

            # Terminate the EC2 instance
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            print(f'Terminated EC2 instance with ID: {instance_id}')

        except Exception as e:
            print(f"An error occurred during instance termination: {str(e)}")

# Main script
if __name__ == '__main__':
    instance_id = launch_ec2_instance()
    terminate_ec2_instance(instance_id)
