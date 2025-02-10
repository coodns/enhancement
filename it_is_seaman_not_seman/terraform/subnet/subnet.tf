resource "aws_subnet" "pub-d" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = var.subnet_cidrblock.pub-d
  enable_dns64                                   = "false"
#   enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
#   map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  vpc_id                                         = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]
}

resource "aws_subnet" "pub-b" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = var.subnet_cidrblock.pub-b
  enable_dns64                                   = "false"
#   enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
#   map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  vpc_id                                         = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]
}

resource "aws_subnet" "priv-a" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = var.subnet_cidrblock.priv-a
  enable_dns64                                   = "false"
#   enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
#   map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "false"
  private_dns_hostname_type_on_launch            = "ip-name"

  tags = {
    Name = "priv-a"
  }

  tags_all = {
    Name = "priv-a"
  }

  vpc_id = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]
}

resource "aws_subnet" "pub-a" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = var.subnet_cidrblock.pub-a
  enable_dns64                                   = "false"
#   enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
#   map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  vpc_id                                         = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]
}

resource "aws_subnet" "pub-c" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = var.subnet_cidrblock.pub-c
  enable_dns64                                   = "false"
#   enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
#   map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  vpc_id                                         = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]
}

resource "aws_subnet" "priv-c" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = var.subnet_cidrblock.priv-c
  enable_dns64                                   = "false"
#   enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
#   map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "false"
  private_dns_hostname_type_on_launch            = "ip-name"

  tags = {
    Name = "priv-c"
  }

  tags_all = {
    Name = "priv-c"
  }

  vpc_id = data.tfe_outputs.vpc.nonsensitive_values["aws_vpc_default_id"]
}

data "tfe_outputs" "vpc" {
  organization = var.organization_name
  workspace    = var.vpc_workspace_name
}

