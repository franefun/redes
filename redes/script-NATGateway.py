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
subnet_id_publica = subnet_publica['Subnet']['SubnetId']

# Habilitar IP pública automática en la subred
ec2.modify_subnet_attribute(
    SubnetId=subnet_id_publica,
    MapPublicIpOnLaunch={'Value': True}
)
print(f"Subred pública creada con ID: {subnet_id_publica}")

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
subnet_id_privada = subnet_publica['Subnet']['SubnetId']
print(f"Subred privada creada con ID: {subnet_id_privada}")


# Creo internet Gateway y lo asocio a la vpc
igw= ec2.create_internet_gateway()
igw_id = igw['InternetGateway']['InternetGatewayId']
ec2.attach_internet_gateway(InternetGatewayId=igw_id,VpcId=vpc_id)
ec2.create_tags(
    Resources=[igw_id],
    Tags=[{'Key': 'Name', 'Value': 'MiIGW'}]
)
print(f"Internet Gateway creado y asociado a la VPC: {igw_id}")


# Creo tabla de rutas
route_table=ec2.create_route_table (VpcId=vpc_id)
rtb_id = route_table['RouteTable']['RouteTableId']
print(f"Tabla de rutas creada: {rtb_id}")


# Creo ruta hacia Internet
ec2.create_route(
    RouteTableId=rtb_id,
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=igw_id
)
print(f"Ruta a Internet creada en la tabla {rtb_id}")

# Asociar la tabla de rutas a la subred pública
association = ec2.associate_route_table(
    SubnetId=subnet_id_publica,
    RouteTableId=rtb_id
)
print(f"Tabla de rutas {rtb_id} asociada a la subred {subnet_id_publica}")



