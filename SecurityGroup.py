import boto3
from botocore.exceptions import ClientError

def create_security_group(security_group_name, description, vpc_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_security_group(GroupName=security_group_name, Description=description, VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
        create_security_group_ingress(security_group_id)
    except ClientError as e:
        print(e)
    
def create_security_group_ingress(security_group_id):
    ec2 = boto3.client('ec2')
    try:
        data = ec2.authorize_security_group_ingress(GroupId=security_group_id,
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
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)
    
                               
