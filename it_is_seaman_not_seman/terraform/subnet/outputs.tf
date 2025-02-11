output "pub-d_id" {
  value = aws_subnet.pub-d.id
}

output "pub-b_id" {
  value = aws_subnet.pub-b.id
}

output "priv-a_id" {
  value = aws_subnet.priv-a.id
}

output "pub-a_id" {
  value = aws_subnet.pub-a.id
}

output "pub-c_id" {
  value = aws_subnet.pub-c.id
}

output "priv-c_id" {
  value = aws_subnet.priv-c.id
}

output "priv-a_cidr" {
  value = aws_subnet.priv-a.cidr_block
}
output "priv-c_cidr" {
  value = aws_subnet.priv-c.cidr_block
}
output "pub-a_cidr" {
  value = aws_subnet.pub-a.cidr_block
}
output "pub-b_cidr" {
  value = aws_subnet.pub-b.cidr_block
}
output "pub-c_cidr" {
  value = aws_subnet.pub-c.cidr_block
}
output "pub-d_cidr" {
  value = aws_subnet.pub-d.cidr_block
}

