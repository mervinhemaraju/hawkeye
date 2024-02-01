##Filter from default bus (prod-legacy)
resource "aws_cloudwatch_event_rule" "tech_role_events_forwarder_eu_west_1" {
  name           = "filter-tech-role-events-${var.env}"
  description    = "filter-tech-role-events-${var.env}"
  is_enabled     = true
  event_bus_name = "default"
  event_pattern = jsonencode(
    {
      source = ["aws.ec2", "aws.secretsmanager", "aws.kms"],
      "detail" : {
        "userIdentity" : {
          "arn" : [{
            "prefix" : "arn:aws:sts::${var.account_id}:assumed-role/tech"
          }]
        }
      }
      region = [var.region]
    }
  )
}

resource "aws_cloudwatch_event_target" "target" {
  arn            = aws_cloudwatch_event_bus.central_bus.arn
  event_bus_name = "default"
  role_arn       = aws_iam_role.cross_region_eventbus.arn
  rule           = aws_cloudwatch_event_rule.tech_role_events_forwarder_eu_west_1.name
  depends_on = [
    aws_cloudwatch_event_bus.central_bus
  ]
}

##Filter from default bus (global services)
resource "aws_cloudwatch_event_rule" "tech_role_events_forwarder_us_east_1" {
  provider       = aws.NorthVirginia
  name           = "filter-global-tech-role-events-${var.env}"
  description    = "filter-global-tech-role-events-${var.env}"
  is_enabled     = true
  event_bus_name = "default"
  event_pattern = jsonencode(
    {
      "detail" : {
        "userIdentity" : {
          "arn" : [{
            "prefix" : "arn:aws:sts::${var.account_id}:assumed-role/tech"
          }]
        }
      }
      region = ["us-east-1"]
      source = ["aws.iam", "aws.route53", "aws.directconnect"]
    }
  )
}

resource "aws_cloudwatch_event_target" "target_global_events" {
  provider       = aws.NorthVirginia
  arn            = aws_cloudwatch_event_bus.central_bus.arn
  event_bus_name = "default"
  role_arn       = aws_iam_role.cross_region_eventbus.arn
  rule           = aws_cloudwatch_event_rule.tech_role_events_forwarder_us_east_1.name
  depends_on = [
    aws_cloudwatch_event_bus.central_bus
  ]
}


### Central Bus

resource "aws_cloudwatch_event_bus" "central_bus" {
  name = "tech-role-events-bus-${var.env}"
}

resource "aws_cloudwatch_event_rule" "tech_role_events" {
  name           = "tech-role-events-${var.env}"
  description    = "tech-role-events-${var.env}"
  is_enabled     = true
  event_bus_name = aws_cloudwatch_event_bus.central_bus.name
  event_pattern = jsonencode(
    {
      account = [
        var.account_id,
      ]
      detail = {
        userIdentity = {
          arn = [
            {
              prefix = "arn:aws:sts::${var.account_id}:assumed-role/tech"
            },
          ]
        },
        eventName = [
          {
            anything-but = "Decrypt"
          }
        ],
      }
    }
  )
}

resource "aws_cloudwatch_event_target" "lambda_attach_tech_role_events" {
  arn            = module.lambda_function_hawkeye.lambda_function_arn
  event_bus_name = aws_cloudwatch_event_bus.central_bus.name
  rule           = aws_cloudwatch_event_rule.tech_role_events.name

  depends_on = [
    aws_cloudwatch_event_rule.tech_role_events
  ]
}
