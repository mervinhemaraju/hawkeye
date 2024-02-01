# Hawkeye

Hawkeye is an event monitoring tool that captures records about specific AWS roles on AWS and then sends them in real-time on a Slack Channel.

## How it works

* All events that are logged in the AWS cloud trail are sent to our EventBus.
* We need to get event records from region **us-east-1** as well because for all AWS services that is offered on a global basis (IAM, Route53, etc.) the records on Cloudtrail are captured there as this is the default region for AWS.
* Eventbridge will match the event records to a **user-defined event pattern.**
* If the event matches our event pattern, the event record will be sent to our Hawkeye lambda
* The lambda will then proceed with the record and **perform some filtering** to get the data needed.
* This data will then be sent to a Slack channel in a human-readable format.

## AWS Services Monitored

The current AWS services that are being monitored are:

* EC2
* Secrets Manager
* KMS
* IAM
* Route 53
* Direct Connect

Other services can be added as well on demand

## Event Pattern

We have two event patterns set up.

### EventBridge Pattern in us-east-1

This has been set up to monitor AWS services found in a global region context

### Event Bridge Pattern in Target Region

This has been set up to monitor all other mentioned AWS services that are not on a global region context
