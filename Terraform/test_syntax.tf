# This file tests syntax highlighting
# It should NOT be included in the final package

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
  
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
  
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 2
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default = {
    Project     = "MyApp"
    ManagedBy   = "Terraform"
  }
}

# Locals
locals {
  common_tags = merge(var.tags, {
    Environment = var.environment
    Timestamp   = timestamp()
  })
  
  # Complex expression
  instance_names = [
    for i in range(var.instance_count) : 
    format("%s-instance-%02d", var.environment, i + 1)
  ]
}

# Data source
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Provider configuration
provider "aws" {
  region = "us-east-1"
  
  default_tags {
    tags = local.common_tags
  }
}

# Resource with for_each
resource "aws_instance" "web" {
  for_each = toset(local.instance_names)
  
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  
  root_block_device {
    volume_size = 20
    volume_type = "gp3"
    encrypted   = true
  }
  
  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }
  
  tags = {
    Name = each.key
  }
  
  lifecycle {
    create_before_destroy = true
    ignore_changes        = [ami]
  }
}

# Dynamic block example
resource "aws_security_group" "web" {
  name_prefix = "${var.environment}-web-"
  description = "Security group for web servers"
  
  dynamic "ingress" {
    for_each = var.environment == "production" ? [80, 443] : [80, 443, 8080]
    
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Module usage
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "${var.environment}-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = local.common_tags
}

# Output with conditional
output "instance_ips" {
  description = "IP addresses of instances"
  value = {
    for k, v in aws_instance.web : k => v.public_ip
  }
}

output "load_balancer_dns" {
  description = "DNS name of load balancer"
  value       = var.environment == "production" ? aws_lb.main[0].dns_name : "N/A"
  sensitive   = false
}

# Terraform functions
locals {
  # String functions
  uppercase_env = upper(var.environment)
  formatted_name = format("%s-%s", var.environment, "app")
  
  # List functions
  first_instance = element(local.instance_names, 0)
  instance_count = length(local.instance_names)
  
  # Map functions
  merged_tags = merge(var.tags, { Extra = "tag" })
  tag_keys = keys(var.tags)
  
  # Conditional
  is_prod = var.environment == "production" ? true : false
  
  # Try/Can
  ami_id = try(data.aws_ami.ubuntu.id, "ami-default")
}

# Moved block (Terraform 1.1+)
moved {
  from = aws_instance.old
  to   = aws_instance.web
}

# Import block (Terraform 1.5+)
import {
  id = "sg-1234567890abcdef0"
  to = aws_security_group.existing
}

# Check block (Terraform 1.5+)
check "health_check" {
  assert {
    condition     = aws_instance.web["${var.environment}-instance-01"].instance_state == "running"
    error_message = "Instance must be running"
  }
}

# Terraform Stacks example (if in .tfstack.hcl file)
# component "networking" {
#   source = "./modules/networking"
#   
#   providers = {
#     aws = aws.primary
#   }
#   
#   inputs = {
#     environment = var.environment
#   }
# }