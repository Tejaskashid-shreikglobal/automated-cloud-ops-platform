# IAM Permission Matrix

## Purpose
Document the AWS permissions defined for the Automated Cloud Operations & Self-Healing Platform.

## Permission Matrix

| Component | Action | Resource Scope | Purpose |
|---|---|---|---|
| Lambda execution role | sqs:ReceiveMessage | Incident SQS queue ARN | Receive incident messages |
| Lambda execution role | sqs:DeleteMessage | Incident SQS queue ARN | Delete successfully processed messages |
| Lambda execution role | sqs:GetQueueAttributes | Incident SQS queue ARN | Read queue attributes |
| Lambda execution role | sqs:ChangeMessageVisibility | Incident SQS queue ARN | Adjust visibility during processing |
| Lambda execution role | dynamodb:PutItem | Incidents DynamoDB table ARN | Save incident records |
| Lambda execution role | logs:CreateLogStream | Configured CloudWatch log group streams | Create log streams |
| Lambda execution role | logs:PutLogEvents | Configured CloudWatch log group streams | Write application logs |

## Permissions Not Intentionally Granted
- No wildcard resource access is intended for the listed data-plane permissions.
- No S3 write permission is included in the current Lambda policy because the handler does not write evidence to S3.
- No permission to modify IAM roles or policies is included in the Lambda execution policy.
- No permission to delete DynamoDB records is included.

## Security Review Notes
- The policy is defined in Terraform and should be reviewed before deployment.
- Confirm that the CloudWatch Logs resource ARN and SQS queue ARN match the intended resources.
- The Lambda service trust policy should allow the Lambda service to assume the execution role.
- The Terraform deployment identity needs separate permissions to provision infrastructure; those permissions are not defined by this Lambda runtime matrix.
- This document describes the intended Terraform policy. It is not proof of permissions deployed in a live AWS account.

## Verification Status
- Terraform validation and plan have succeeded locally.
- Live IAM policy simulation and deployed-role verification have not been performed.
- No AWS deployment is claimed.
