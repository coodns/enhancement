resource "aws_nat_gateway" "natgw" {
  allocation_id                      = "eipalloc-0cc87bcf2ce557a34"
  connectivity_type                  = "public"
  private_ip                         = "172.31.12.175"
  subnet_id                          = "subnet-069d727065bc8d394"

  tags = {
    Name = "default-nat"
  }

  tags_all = {
    Name = "default-nat"
  }
}
resource "aws_internet_gateway" "igw" {
  vpc_id = "vpc-0c597f06ab2d6ae50"
}
