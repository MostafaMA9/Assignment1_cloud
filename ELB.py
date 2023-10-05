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


def create_load_balancer(client, name, security_group_id, subnets):
    try:
        response = client.create_load_balancer(
            Name=name, 
            SecurityGroups=[security_group_id], 
            Subnets=subnets, 
            Scheme='internet-facing', 
            Type='application', 
            IpAddressType='ipv4', 
            Tags=[{'Key': 'Name', 'Value': name}], 
            # TargetGroupArn=target_group_arns)
        )
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

# register instances to respective target groups
def register_instances_to_target_groups(client, m4instancesId, t2instancesId, tg_cluster1, tg_cluster2):
    print("registering 5 m4.large instances to target group 1 and 4 t2.large instances to target group 2")
    
    m4Targets = []
    for m4Instance in m4instancesId:
        m4Targets.append({'Id': m4Instance})
    
    client.register_targets(
        TargetGroupArn=tg_cluster1.get('TargetGroups')[0].get('TargetGroupArn'),
        Targets=m4Targets
    )

    t2Targets = []
    for t2Instance in t2instancesId:
        t2Targets.append({'Id': t2Instance})
        
    client.register_targets(
        TargetGroupArn=tg_cluster2.get('TargetGroups')[0].get('TargetGroupArn'),
        Targets=t2Targets
    )
    
# Unregister instances to respective target groups in teardown
def unregister_instances_from_target_groups(client, m4instancesId, t2instancesId, tg_cluster1, tg_cluster2):
    print("Deregistering instances from target group")
    
    m4Targets = []
    for m4Instance in m4instancesId:
        m4Targets.append({'Id': m4Instance})
    
    client.deregister_targets(
        TargetGroupArn=tg_cluster1.get('TargetGroups')[0].get('TargetGroupArn'),
        Targets=m4Targets
    )

    t2Targets = []
    for t2Instance in t2instancesId:
        t2Targets.append({'Id': t2Instance})
        
    client.deregister_targets(
        TargetGroupArn=tg_cluster2.get('TargetGroups')[0].get('TargetGroupArn'),
        Targets=t2Targets
    )
    


def delete_target_group(elvb2, target_group_arn):
    try:
        response = elvb2.delete_target_group(TargetGroupArn=target_group_arn)
        return response
    except ClientError as e:
        print(e)

def delete_load_balancer(elvb2, load_balancer_arn):
    try:
        response = elvb2.delete_load_balancer(LoadBalancerArn=load_balancer_arn)
        return response
    except ClientError as e:
        print(e)

def delete_listener(elvb2, listener_arn):
    try:
        response = elvb2.delete_listener(ListenerArn=listener_arn)
        return response
    except ClientError as e:
        print(e)

def delete_rule(elvb2, rule_arn):
    try:
        response = elvb2.delete_rule(RuleArn=rule_arn)
        return response
    except ClientError as e:
        print(e)