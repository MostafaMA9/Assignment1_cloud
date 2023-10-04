import boto3
from botocore.exceptions import ClientError

def create_security_group(ec2, security_group_name, description, vpc_id):
    try:
        response = ec2.create_security_group(GroupName=security_group_name, Description=description, VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
        create_security_group_ingress(ec2, security_group_id)
        return response
    except ClientError as e:
        print(e)
    
def create_security_group_ingress(ec2, security_group_id):
    try:
        response = ec2.authorize_security_group_ingress(GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        return response
    except ClientError as e:
        print(e)
    
                               
