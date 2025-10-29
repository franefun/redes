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

    #Crear una subnet
    SUB_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 192.168.0.0/28 \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=Mi-Subred1.fran}]' \
    --query 'Subnet.SubnetId' \
    --output text)

    #Muestro la id de la subnet
    echo $SUB_ID

    #Habilita la asignación de la ipv4publica en la subred
    #Comprobar como NO se habilita y tenemos que hacerlo a posteriori
    aws ec2 modify-subnet-attribute --subnet-id $SUB_ID --map-public-ip-on-launch
