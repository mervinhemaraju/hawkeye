# Get the Lambda ARN as output
output "lambda_function_hawkeye_arn" {
  value = module.lambda_function_hawkeye.lambda_function_arn
}
