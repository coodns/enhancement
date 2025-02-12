resource "aws_network_interface" "for_natgw" {
  description        = "Interface for NAT Gateway nat-0d142135433605fd9"
  source_dest_check  = "false"
  subnet_id          = data.tfe_outputs.subnet.nonsensitive_values["pub-a_id"]
}