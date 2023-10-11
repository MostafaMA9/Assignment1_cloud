# Here we create 4 M4.large instances for cluster 1. 

def create_m4large_instances(client, keyPair, securityGroupId, subnetId):
    print('Creating 4 instances of m4.large...')
    lowercase_a = 97
    ids = []
    
    for instance in range(4):
        response = client.run_instances(

            ImageId='ami-08c40ec9ead489470',
            InstanceType='m4.large',
            KeyName=keyPair,
            UserData=open('setup.sh').read(),
            SubnetId=subnetId,
            SecurityGroupIds=[
                securityGroupId,
            ],
            MaxCount=1,
            MinCount=1,
            Monitoring={   
                'Enabled': True
            },
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'cluster1' + chr(lowercase_a + instance)
                        },
                    ]
                },
            ],
        )
        ids.append(response["Instances"][0]["InstanceId"])
        
    return ids


 # Here we create 5 t2.large instances for cluster 2. 
 
def create_t2large_instances(client, keyPair, securityGroupId, subnetId):
    print('Creating 5 instances of t2.large...')
    lowercase_a = 97
    ids = []

    for instance in range(5):
        response = client.run_instances(

            ImageId='ami-08c40ec9ead489470',
            InstanceType='t2.large',
            KeyName=keyPair,
            UserData=open('setup.sh').read(),
            SubnetId=subnetId,
            SecurityGroupIds=[
                securityGroupId,
            ],
            MaxCount=1,
            MinCount=1,
            Monitoring={
                'Enabled': True
            },
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'cluster2' + chr(lowercase_a + instance)
                        },
                    ]
                },
            ],
        )
        ids.append(response["Instances"][0]["InstanceId"])
        
    return ids
    

# This function terminates the running instances ".
def terminate_instance(client, instanceIds):
    print('terminating cluster of instances:')
    print(instanceIds)
    client.terminate_instances(InstanceIds=(instanceIds))

