#create key_pair
def create_key_pair(ec2_client, key_pair_name):
    """
    Make key pair to be able to connect to instances

    :returns: The key pair's name
    """
    # Create a key pair (if not already created)
    try:
        key_pair = ec2_client.create_key_pair(KeyName=key_pair_name)
        # Save the PEM file locally
        with open(f'{key_pair_name}.pem', 'w') as pem_file:
            pem_file.write(key_pair['KeyMaterial'])
        print(f'Key pair {key_pair_name} created and PEM file saved as {key_pair_name}.pem')
    except ec2_client.exceptions.ClientError as e:
        if 'KeyPair' in str(e):
            print(f'Key pair {key_pair_name} already exists.')
        else:
            raise
    
    return key_pair['KeyName']


# Delete the key pair

def delete_key_pair(ec2_client,  key_pair_name):

    try:
        ec2_client.delete_key_pair(KeyName=key_pair_name)
        print(f'Deleted key pair: {key_pair_name}')
    except ec2_client.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            print(f'Key pair {key_pair_name} does not exist.')
        else:
            raise
