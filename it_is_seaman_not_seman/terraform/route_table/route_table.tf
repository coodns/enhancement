resource "aws_route_table" "priv_route" {
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = "nat-0d142135433605fd9"
  }

  route {
    cidr_block         = "10.10.0.0/16"
    transit_gateway_id = "tgw-01a8e081494143de9"
  }

  route {
    cidr_block         = "20.0.0.0/16"
    transit_gateway_id = "tgw-01a8e081494143de9"
  }

  tags = {
    Name = "priv"
  }

  tags_all = {
    Name = "priv"
  }

  vpc_id = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]

}

resource "aws_route_table" "pub_route" {
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "igw-065962980f949cee8"
  }

  vpc_id = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]
}


resource "aws_main_route_table_association" "vpc_association" {
  route_table_id = aws_route_table.pub_route.id
  vpc_id         = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]
}



data "tfe_outputs" "vpc" {
  organization = var.organization_name
  workspace    = var.vpc_workspace_name
}
