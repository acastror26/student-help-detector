variable "aws_region" {
  default = "us-west-2"
}

variable "db_instance_class" {
  default = "db.t2.micro"
}

variable "db_allocated_storage" {
  default = 20
}

variable "db_username" {
  default = "postgres"
}

variable "db_password" {
  default = "password"
}

variable "elasticsearch_version" {
  default = "7.9"
}

variable "instance_type" {
  default = "t3.small.elasticsearch"
}

variable "ebs_volume_size" {
  default = 10
}
