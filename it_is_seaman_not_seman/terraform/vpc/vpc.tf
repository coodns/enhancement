resource "aws_vpc" "default" {
  assign_generated_ipv6_cidr_block     = "false"
  cidr_block                           = var.vpc_cidr_block
  enable_dns_hostnames                 = "true"
  enable_dns_support                   = "true"
  enable_network_address_usage_metrics = "false"
  instance_tenancy                     = "default"
}
