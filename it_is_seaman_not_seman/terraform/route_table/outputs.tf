output "vpc_association" {
  value = aws_main_route_table_association.vpc_association.id
}

output "pub_d_rt_association_id" {
  value = aws_route_table_association.pub-d-rt-to-pub-rt.id
}

output "pub_b_rt_association_id" {
  value = aws_route_table_association.pub-b-rt-to-pub-rt.id
}

output "priv_a_rt_association_id" {
  value = aws_route_table_association.priv-a-rt-to-priv-rt.id
}

output "pub_c_rt_association_id" {
  value = aws_route_table_association.pub-c-rt-to-pub-rt.id
}

output "pub_a_rt_association_id" {
  value = aws_route_table_association.pub-a-rt-to-pub-rt.id
}

output "priv_c_rt_association_id" {
  value = aws_route_table_association.priv-c-rt-to-priv-rt.id
}

output "priv_rt_id" {
  value = aws_route_table.priv_route.id
}

output "pub_rt_id" {
  value = aws_route_table.pub_route.id
}

output "eni_for_natgw_id" {
  value = "${aws_network_interface.for_natgw.id}"
}

output "eip_natgw_id" {
  value = "${aws_eip.eip_natgw.id}"
}

