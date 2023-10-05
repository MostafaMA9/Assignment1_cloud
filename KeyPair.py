#create key_pair
def create_key_pair(ec2_client, keypair_name):
    """
    Make key pair to be able to connect to instances

    :returns: The key pair's name
    """
    key_pair = ec2_client.create_key_pair(
    KeyName=keypair_name,
    KeyType='rsa',
    KeyFormat='ppk'
    )
    return key_pair['KeyName']

def delete_key_pair(ec2_client,  keypair_name):

    ec2_client.delete_key_pair(KeyName=keypair_name)
