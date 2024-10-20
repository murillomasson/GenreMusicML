aws_ami            = "ami-0866a3c8686eaeeba"
instance_type      = "t2.micro"

db_identifier      = "db-spotify-ml-proj"
db_allocated_storage = 20               
db_engine          = "postgres"        
db_instance_class  = "db.t2.micro"     
db_name            = "postgres"
db_username        = "postgres"
db_password        = "eS}T>Dij3620)&57L("

cidr_block         = "172.31.0.0/16"
subnet_cidr_block  = "10.0.1.0/24"

allowed_ip         = "187.10.245.47/32"       

region             = "us-east-1"       

spotify_client_id     = "a6aaec81803f433e83db1265d3ca511b"
spotify_client_secret = "f61bd8e2f24142d2bc2e2c7f40589a64"
