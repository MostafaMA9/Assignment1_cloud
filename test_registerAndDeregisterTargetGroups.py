import boto3
import os
from dotenv import load_dotenv
from time import time

from ELB import *
from SecurityGroup import *
from KeyPair import *
from botocore.exceptions import ClientError

load_dotenv("./credentials")
aws_access_key_id = os.environ["aws_access_key_id"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
aws_session_token = os.environ["aws_session_token"]

# Define EC2 instance parameters
keyPairName = 'LOG8415E'
securityGroupName = 'LOG8415E_LAB_B2'



def get_all_ec2_instances():
    ec2 = boto3.client('ec2', region_name="us-east-1")
    response = ec2.describe_instances()
    list_ec2_instance_m4Large=[]
    list_ec2_instance_t2Large=[]
    
    for ec2_instance in response['Reservations']:
        ec2_instance_Id = ec2_instance['Instances'][0]['InstanceId'] 
        ec2_instance_Type = ec2_instance['Instances'][0]['InstanceType']
        if(ec2_instance_Type == "m4.large"):
            dictionary = {}
            dictionary['Id'] = ec2_instance_Id
            list_ec2_instance_m4Large.append(dictionary)
            continue
        if(ec2_instance_Type == "t2.large"):
            dictionary={}
            dictionary['Id'] = ec2_instance_Id
            list_ec2_instance_t2Large.append(dictionary)

    return list_ec2_instance_m4Large, list_ec2_instance_t2Large


# get the target group Arn
def get_targetGroupArn(elvb2):
    list_target_groups_Arn = []
    for tg in elvb2.describe_target_groups()['TargetGroups']:
        print("the target group Arn for "+tg['TargetGroupName']+ " was found...")
        list_target_groups_Arn.append(tg['TargetGroupArn'])
    return list_target_groups_Arn



def register_targets(elvb2, target_groups_Arn, list_ec2_instance):
    response = elvb2.register_targets(
        TargetGroupArn = target_groups_Arn,
        Targets = list_ec2_instance,
    )
    print(response)


def deregister_targets(elvb2, target_groups_Arn, list_ec2_instance):
    response = elvb2.deregister_targets(
        TargetGroupArn = target_groups_Arn,
        Targets = list_ec2_instance,
    )
    print(response)
    

if __name__ == '__main__':
    ELBV2 = boto3.client(
    'elbv2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
    )
    
    list_ec2_instance_m4Large, list_ec2_instance_t2Large = get_all_ec2_instances() 
    list_target_groups_Arn = get_targetGroupArn(ELBV2)


    register_targets(ELBV2, list_target_groups_Arn[0], list_ec2_instance_m4Large)
    register_targets(ELBV2, list_target_groups_Arn[1], list_ec2_instance_t2Large)

    deregister_targets(ELBV2, list_target_groups_Arn[0], list_ec2_instance_m4Large)
    deregister_targets(ELBV2, list_target_groups_Arn[1], list_ec2_instance_t2Large)


