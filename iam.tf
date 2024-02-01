resource "aws_iam_role_policy" "cross_region_eventbus_policy" {
  name = "my_cross_region_eventbus-${var.env}_policy"
  role = aws_iam_role.cross_region_eventbus.id

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Effect" : "Allow",
        "Action" : [
          "events:PutEvents"
        ],
        "Resource" : [
          aws_cloudwatch_event_bus.central_bus.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role" "cross_region_eventbus" {
  name = "my_cross_region_eventbus-${var.env}_role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = "VisualEditor0"
        Principal = {
          Service = "events.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_policy" {

  name        = "${var.function_name}-${var.env}-execution-policy"
  path        = "/"
  description = "The execution IAM role for Hakweye"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "VisualEditor0",
        "Effect" : "Allow",
        "Action" : "secretsmanager:GetSecretValue",
        "Resource" : "arn:aws:secretsmanager:${var.region}:${var.account_id}:secret:sysops/${var.env}/hawkeye-??????"
      }
    ]
  })
}
