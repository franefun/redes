import boto3
import time

# Crear cliente EC2
ec2 = boto3.client('ec2')

# Crear la VPC
vpc_response = ec2.create_vpc(
    CidrBlock='192.168.0.0/16',
    TagSpecifications=[
        {
            'ResourceType': 'vpc',
            'Tags': [{'Key': 'Name', 'Value': 'MyVpc'}]
        }
    ]
)
vpc_id = vpc_response['Vpc']['VpcId']
print(f"VPC creada con ID: {vpc_id}")

# Habilitar DNS en la VPC
ec2.modify_vpc_attribute(
    VpcId=vpc_id,
    EnableDnsHostnames={'Value': True}
)
print("DNS hostnames habilitados en la VPC.")

subnet_publica= ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='192.168.0.0/24',
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [{'Key': 'Name', 'Value': 'MiSubred-publica'}]
        }
    ]
)
subnet_id = subnet_publica['Subnet']['SubnetId']

# Habilitar IP pública automática en la subred
ec2.modify_subnet_attribute(
    SubnetId=subnet_id,
    MapPublicIpOnLaunch={'Value': True}
)
print(f"Subred pública creada con ID: {subnet_id}")

subnet_privada= ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='192.168.1.0/24',
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [{'Key': 'Name', 'Value': 'MiSubred-privada'}]
        }
    ]
)
subnet_id = subnet_publica['Subnet']['SubnetId']
print(f"Subred privada creada con ID: {subnet_id}")




