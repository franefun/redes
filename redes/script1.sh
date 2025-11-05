
# Crear una VPC y devolver su ID
VPC_ID=$(aws ec2 create-vpc \
  --cidr-block 192.168.0.0/24 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=MyVpc}]' \
  --query 'Vpc.VpcId' \
  --output text)

echo "VPC creada con ID: $VPC_ID"

# Habilitar DNS en la VPC
aws ec2 modify-vpc-attribute \
  --vpc-id "$VPC_ID" \
  --enable-dns-hostnames "{\"Value\":true}"

# Crear subred dentro de la VPC
SUB_ID=$(aws ec2 create-subnet \
  --vpc-id "$VPC_ID" \
  --cidr-block 192.168.0.0/28 \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=MiSubred1}]' \
  --query 'Subnet.SubnetId' \
  --output text)

echo "Subred creada con ID: $SUB_ID"

aws ec2 modify-subnet-attribute --subnet-id $SUB_ID --map-public-ip-on-launch

# Crear Security Group
SG_ID=$(aws ec2 create-security-group \
  --vpc-id $VPC_ID \
  --group-name gs-mck \
  --description "My security group for port 22" \
  --output text)

echo "Security Group creado con ID: $SG_ID"

# Autorizar el puerto 22 (ssh) para ese SG // esto no le gusta
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# Crear EC2 (ejemplo 1)
EC2_ID=$(aws ec2 run-instances \
    --image-id ami-0360c520857e3138f \
    --instance-type t3.micro \
    --key-name vockey \
    --subnet-id $SUB_ID \
    --associate-public-ip-address \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=miEc2}]' \
    --query Instance.InstanceId --output text)

sleep 15

echo "EC2 creada con ID: $EC2_ID"