output "ec2_public_ip" {
  value = aws_instance.pyspark_ec2.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.rds_postgres.endpoint
}
