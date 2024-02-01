# Hawkeye Lambda Function
module "lambda_function_hawkeye" {

  # * Lambda module configs
  source  = "terraform-aws-modules/lambda/aws"
  version = "3.0.0"

  # * Lambda Configs
  function_name                     = "${var.function_name}-${var.env}"
  description                       = "The lambda for the Hawkeye Project"
  handler                           = local.constants.lambda.HANDLER
  runtime                           = local.constants.lambda.VERSION
  attach_policies                   = true
  number_of_policies                = 1
  memory_size                       = 128
  cloudwatch_logs_retention_in_days = 14
  policies                          = [aws_iam_policy.lambda_policy.arn]
  source_path                       = "./function/"
  timeout                           = local.constants.lambda.TIMEOUT
  create_async_event_config         = true
  maximum_retry_attempts            = local.constants.lambda.RETRIES_ATTEMPT

  # * VPC configurations
  vpc_subnet_ids         = data.aws_subnets.sysops_vpc_private_subnets.ids
  vpc_security_group_ids = [data.aws_security_group.vpc_endpoint_sysops_vpc.id]
  attach_network_policy  = true

  layers = [
    data.aws_lambda_layer_version.layer_requests.arn
  ]

  environment_variables = {
    AWS_ACCOUNT = var.env
  }

  tags = {
    Name = "${var.function_name}-${var.env}"
  }

  trusted_entities = local.constants.lambda.TRUSTED_ENTITIES
}


# Lambda Permission Triggers
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function_hawkeye.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.tech_role_events.arn
}
