# Get the Layer for requests library
data "aws_lambda_layer_version" "layer_requests" {
  layer_name = local.constants.datasources.LAYER_LIBRARY_REQUESTS
}

data "aws_security_group" "vpc_endpoint_my_vpc" {
  filter {
    name   = "tag:Name"
    values = ["outbound-traffic-my-vpc"]
  }
}

data "aws_vpc" "my_vpc" {
  filter {
    name   = "tag:Name"
    values = ["my-vpc"]
  }
}

data "aws_subnets" "my_vpc_private_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.my_vpc.id]
  }

  tags = {
    Tier = "Private"
  }
}
