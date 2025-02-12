resource "aws_eip" "eip_natgw" {
  domain               = "vpc"
  network_border_group = "ap-northeast-2"
  network_interface    = aws_network_interface.for_natgw.id
  public_ipv4_pool     = "amazon"
}
