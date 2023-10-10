def create_security_group(ec2_client, security_group_name, vpc_id):
    try:
        security_group = ec2_client.create_security_group(
            Description='FlaskApp Security Group',
            GroupName=security_group_name,
            VpcId=vpc_id
        )

        response = ec2_client.describe_security_groups(
        GroupNames=[security_group_name]
        )
        security_group_id = response['SecurityGroups'][0]['GroupId']

        # Add inbound rules to allow SSH (port 22) and HTTP (port 80) traffic
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,  # SSH port
                    'ToPort': 22,    # SSH port
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Allow SSH from any IP
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,  # HTTP port
                    'ToPort': 80,    # HTTP port
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Allow HTTP from any IP
                }
            ]
        )

    except ec2_client.exceptions.ClientError as e:
        if 'already exists' in str(e):
            print(f'Security group {security_group_name} already exists.')
        else:
            raise

    return security_group


# Delete the security group

def delete_security_group(ec2_client, security_group_name):
    try:
        ec2_client.delete_security_group(GroupName=security_group_name)
        print(f'Deleted security group: {security_group_name}')
    except ec2_client.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            print(f'Security group {security_group_name} does not exist.')
        else:
            raise