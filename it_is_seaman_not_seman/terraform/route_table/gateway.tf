resource "aws_nat_gateway" "natgw" {
  allocation_id     = aws_eip.eip_natgw.id
  connectivity_type = "public"
  subnet_id         = data.tfe_outputs.subnet.nonsensitive_values["pub-a_id"]

  tags = {
    Name = "default-nat"
  }

  tags_all = {
    Name = "default-nat"
  }
}
resource "aws_internet_gateway" "igw" {
  vpc_id = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]
}
