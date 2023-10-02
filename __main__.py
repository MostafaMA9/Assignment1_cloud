from SecurityGroup import *
from ELB import *
from instances import *
from KeyPair import *

def main():
    create_vpc(1,'')
    create_subnet(1,'',1)
    create_subnet(2,'',1)

    create_security_group('my-security-group', 'My security group', 'vpc-0b0b0b0b0b0b0b0b0')
    create_key_pair('my-key-pair')

    create_instances('ami-0b898040803850657', 't2.large', 4, 1, 'my-security-group', 'my-key-pair')
    create_instances('ami-0b898040803850657', 'm4.large', 5, 2,'my-security-group', 'my-key-pair')
