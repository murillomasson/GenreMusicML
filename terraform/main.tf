provider "aws" {
  region = var.aws_region 
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_security_group" "ec2_security_group" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "pyspark_ec2" {
  ami                    = var.aws_ami
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.ec2_security_group.id]
  tags = {
    Name = "PySpark EC2"
  }
}

resource "aws_db_instance" "rds_postgres" {
  identifier             = var.db_identifier
  allocated_storage      = var.db_allocated_storage
  engine                 = var.db_engine
  instance_class         = var.db_instance_class
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  vpc_security_group_ids  = [aws_security_group.ec2_security_group.id]
  skip_final_snapshot    = true
}

resource "null_resource" "copy_main_script" {
  provisioner "file" {
    source      = "main.py"
    destination = "/home/ec2-user/main.py"

    connection {
      type        = "ssh"
      host        = aws_instance.pyspark_ec2.public_ip
      user        = "ec2-user"
      private_key = file("~/.ssh/id_rsa")
    }
  }

  depends_on = [aws_instance.pyspark_ec2]
}

resource "null_resource" "populate_db" {
  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      host        = aws_instance.pyspark_ec2.public_ip
      user        = "ec2-user"
      private_key = file("~/.ssh/id_rsa")
    }

    inline = [
      "python3 /home/ec2-user/main.py"
    ]
  }

  depends_on = [null_resource.copy_main_script]
}
