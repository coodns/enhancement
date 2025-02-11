resource "aws_route_table_association" "pub-a-rt-to-pub-rt" {
  route_table_id = aws_route_table.pub_route.id
  subnet_id      = data.tfe_outputs.subnet.nonsensitive_values["pub-a_id"]
}
resource "aws_route_table_association" "pub-b-rt-to-pub-rt" {
  route_table_id = aws_route_table.pub_route.id
  subnet_id      = data.tfe_outputs.subnet.nonsensitive_values["pub-b_id"]
}
resource "aws_route_table_association" "pub-c-rt-to-pub-rt" {
  route_table_id = aws_route_table.pub_route.id
  subnet_id      = data.tfe_outputs.subnet.nonsensitive_values["pub-c_id"]
}
resource "aws_route_table_association" "pub-d-rt-to-pub-rt" {
  route_table_id = aws_route_table.pub_route.id
  subnet_id      = data.tfe_outputs.subnet.nonsensitive_values["pub-d_id"]
}

resource "aws_route_table_association" "priv-a-rt-to-priv-rt" {
  route_table_id = aws_route_table.priv_route.id
  subnet_id      = data.tfe_outputs.subnet.nonsensitive_values["priv-a_id"]
}
resource "aws_route_table_association" "priv-c-rt-to-priv-rt" {
  route_table_id = aws_route_table.priv_route.id
  subnet_id      = data.tfe_outputs.subnet.nonsensitive_values["priv-c_id"]
}



data "tfe_outputs" "subnet" {
  organization = var.organization_name
  workspace    = var.subnet_workspace_name
}

