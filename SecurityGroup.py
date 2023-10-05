#create security group
def create_security_group(ec2_client, sg_name, vpc_id):
    
    security_group = ec2_client.create_security_group(
        Description="TP1 Security Group",
        GroupName=sg_name,
        VpcId=vpc_id
    )
    # add_inbound_rules(ec2_client, security_group['GroupId'])
    return security_group

#add inbound rules
# def add_inbound_rules(ec2_client, sg_id):
#     """
#     Function that assigns inbound rules to the security group

#     :param ec2_client: The ec2 client that will assign rules
#     :param sg_id: Security group's id
#     """

#     inbound_rules = [
#         {
#             'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22,
#             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
#         },
#         {
#             'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
#             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
#         },
#         {
#             'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443,
#             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
#         }
#         ]
#     ec2_client.authorize_security_group_ingress(GroupId=sg_id, IpPermissions=inbound_rules)

#Delete security group
def delete_security_group(ec2_client, sg_name, vpc_id):

    security_group = ec2_client.delete_security_group(
        Description="TP1 Security Group",
        GroupName=sg_name,
        VpcId=vpc_id
    )