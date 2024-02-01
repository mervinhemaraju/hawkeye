
# Terraform Provider for AWS for the connection
provider "aws" {

  # The AWS Environment Configurations
  region = var.region

  assume_role {
    role_arn = var.assume_role_arn
  }

  # The Default Tags
  default_tags {

    tags = {
      Environment = var.env
      Owner       = local.tags.owner
      Project     = local.tags.project
      Team        = local.tags.team
    }
  }
}


provider "aws" {

  # The AWS Environment Configurations
  region = "us-east-1"
  alias  = "NorthVirginia"

  assume_role {
    role_arn = var.assume_role_arn
  }

  # The Default Tags
  default_tags {

    tags = {
      Environment = var.env
      Owner       = local.tags.owner
      Project     = local.tags.project
      Team        = local.tags.team
    }
  }
}


# The Terraform Module
terraform {

  # Terraform version
  required_version = ">= 1.0.0"

  # AWS Provider
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.8.0"
    }
  }

  # Backend Configuration for S3
  backend "s3" {}
}
