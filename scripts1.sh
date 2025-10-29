#Creo la vpc y devuelve la id
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block 192.168.0.0/24 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=MyVpc}]' \
    --query 'Vpc.VpcId' \
    --output text)

    #Muestro el id de la vpc
    echo $VPC_ID
    #habilitar dns en la vpc
    aws ec2 modify-vpc-attribute \
    --vpc-id $VPC_ID \
    --enable-dns-hostnames "{\"Value\":true}"
