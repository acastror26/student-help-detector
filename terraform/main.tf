provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "main_subnet" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_security_group" "allow_all" {
  name_prefix = "allow_all_traffic"
  description = "Allow all inbound and outbound traffic"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "postgres_db" {
  identifier          = "student-reports-db"
  engine              = "postgres"
  instance_class      = "db.t2.micro"
  allocated_storage   = 20
  name                = "student_reports"
  username            = "postgres"
  password            = "password"
  vpc_security_group_ids = [aws_security_group.allow_all.id]
  db_subnet_group_name   = aws_db_subnet_group.main_subnet_group.id

  skip_final_snapshot = true
}

resource "aws_db_subnet_group" "main_subnet_group" {
  name       = "main-subnet-group"
  subnet_ids = [aws_subnet.main_subnet.id]
}

resource "aws_elasticsearch_domain" "elasticsearch_domain" {
  domain_name = "student-reports-es"

  elasticsearch_version = "7.9"
  cluster_config {
    instance_type = "t3.small.elasticsearch"
  }
  ebs_options {
    ebs_enabled = true
    volume_size = 10
  }
  access_policies = <<CONFIG
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": "*"
        },
        "Action": "es:*",
        "Resource": "arn:aws:es:${aws_region}:${account_id}:domain/student-reports-es/*"
      }
    ]
  }
CONFIG
}

resource "aws_ecs_cluster" "fastapi_cluster" {
  name = "fastapi-app-cluster"
}

resource "aws_ecs_task_definition" "fastapi_task" {
  family                   = "fastapi-app-task"
  container_definitions    = <<DEFINITION
[
  {
    "name": "fastapi-app",
    "image": "your-fastapi-app-image",
    "memory": 512,
    "cpu": 256,
    "essential": true,
    "portMappings": [
      {
        "containerPort": 8000,
        "hostPort": 8000
      }
    ]
  }
]
DEFINITION
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = "512"
  cpu                      = "256"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      }
    }
  ]
}
POLICY
}
