variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "us-east-1"
}

variable "aws_ami" {
  description = "ID da AMI para a instância EC2"
  type        = string
}

variable "db_identifier" {
  description = "Identificador do banco de dados"
  type        = string
  default     = "my-postgres-db"
}

variable "db_allocated_storage" {
  description = "Armazenamento alocado para o banco de dados"
  type        = number
  default     = 20
}

variable "db_engine" {
  description = "Tipo de banco de dados"
  type        = string
  default     = "postgres"
}

variable "db_instance_class" {
  description = "Classe da instância do banco de dados"
  type        = string
  default     = "db.t2.micro"
}

variable "db_name" {
  description = "Nome do banco de dados"
  type        = string
  default     = "mydb"
}

variable "db_username" {
  description = "Nome de usuário do banco de dados"
  type        = string
}

variable "db_password" {
  description = "Senha do banco de dados"
  type        = string
  sensitive   = true
}

variable "spotify_client_id" {
  description = "Client ID for Spotify API"
  type        = string
}

variable "spotify_client_secret" {
  description = "Client Secret for Spotify API"
  type        = string
}