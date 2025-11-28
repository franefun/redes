import boto3
import time

# Crear cliente EC2
ec2 = boto3.client('ec2')

# Crear la VPC
vpc_response = ec2.create_vpc(
    CidrBlock='192.168.0.0/24',
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

# Crear Subred
subnet_response = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='192.168.0.0/28',
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [{'Key': 'Name', 'Value': 'MiSubred1'}]
        }
    ]
)
subnet_id = subnet_response['Subnet']['SubnetId']
print(f"Subred creada con ID: {subnet_id}")

# Habilitar IP pública automática en la subred
ec2.modify_subnet_attribute(
    SubnetId=subnet_id,
    MapPublicIpOnLaunch={'Value': True}
)
print("Subred configurada para asignar IP pública automáticamente.")

# Crear Security Group
sg_response = ec2.create_security_group(
    GroupName='gs-fran',
    Description='My security group for port 22',
    VpcId=vpc_id,
    TagSpecifications=[
        {
            'ResourceType': 'security-group',
            'Tags': [{'Key': 'Name', 'Value': 'gs-fran'}]
        }
    ]
)
sg_id = sg_response['GroupId']
print(f"Security Group creado con ID: {sg_id}")

# Autorizar tráfico SSH (puerto 22)
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)
print("Regla de entrada SSH (22/tcp) agregada al Security Group.")

# Crear instancia EC2
ec2_response = ec2.run_instances(
    ImageId='ami-0360c520857e3138f', 
    InstanceType='t3.micro',
    KeyName='vockey', 
    SubnetId=subnet_id,
    SecurityGroupIds=[sg_id],
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'miEc2'}]
        }
    ],
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'SubnetId': subnet_id,
            'DeviceIndex': 0,
            'Groups': [sg_id]
        }
    ]
)

# Esperar a que la instancia se inicie
instance_id = ec2_response['Instances'][0]['InstanceId']
print(f"EC2 creada con ID: {instance_id}")
print("Esperando 15 segundos para inicialización...")
time.sleep(15)
print("Instancia EC2 lista.")
