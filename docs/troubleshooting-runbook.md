# Troubleshooting Runbook
## Automated Cloud Operations & Self-Healing Platform

### 1. Purpose

This runbook explains how to diagnose and recover from common incident-processing failures. The current project has been tested locally; AWS-specific procedures below are operational guidance and have not been verified against a deployed environment.

### 2. Incident Validation Failure

**Symptoms**
- Missing required fields.
- Invalid timestamp.
- Unsupported incident type.

**Diagnosis**
1. Inspect the incident JSON.
2. Confirm `incident_id`, `timestamp`, `resource_name`, `incident_type`, and `description` are present and non-empty.
3. Confirm the timestamp is ISO 8601 compatible.
4. Confirm the incident type is supported by the incident engine.

**Recovery**
- Correct the malformed input.
- Re-run the relevant local test.
- Preserve the original failure details for audit purposes.

### 3. Lambda Handler Failure

**Symptoms**
- Lambda invocation reports an error.
- Incident processing stops unexpectedly.

**Diagnosis**
1. Check whether `INCIDENT_TABLE` is configured.
2. Inspect the Lambda error message.
3. Verify the handler is configured as `lambda_handler.lambda_handler`.
4. Verify the deployment ZIP contains `lambda_handler.py` and `incident_engine.py` at its root.
5. Review the function's execution role and required permissions.

**Recovery**
- Correct the environment variable, handler configuration, package, or IAM policy as applicable.
- Re-run local tests before considering deployment changes.

### 4. DynamoDB Write Failure

**Symptoms**
- Incident records are not stored.
- Conditional writes fail for an existing incident ID.

**Diagnosis**
1. Verify the configured table name.
2. Verify the execution role has `dynamodb:PutItem` permission on the intended table.
3. Check whether the incident ID already exists.
4. Distinguish duplicate-write errors from other database failures.

**Recovery**
- Correct the table configuration or narrowly scoped permission.
- Handle duplicate delivery idempotently in the application before treating it as successful.
- Do not retry indefinitely.

### 5. SQS Retry and Dead-Letter Queue

**Symptoms**
- Messages are repeatedly delivered.
- Messages eventually appear in the DLQ.

**Diagnosis**
1. Inspect the source queue's redrive policy.
2. Confirm the DLQ ARN and maximum receive count.
3. Review the message body and Lambda error.
4. Check the event source mapping and required SQS permissions.

**Recovery**
- Fix the underlying processing error before redriving a message.
- Preserve the original message and failure details.
- Redrive only after confirming the cause is resolved.
- Avoid repeatedly replaying a known malformed message.

**Note:** DLQ behavior has not yet been verified against a deployed AWS queue.

### 6. Terraform Validation or Plan Failure

**Symptoms**
- `terraform fmt -check` fails.
- `terraform validate` reports invalid configuration.
- `terraform plan` reports provider, permission, or configuration errors.

**Diagnosis**
1. Run `terraform -chdir=terraform fmt -recursive`.
2. Run `terraform -chdir=terraform init -backend=false`.
3. Run `terraform -chdir=terraform validate`.
4. Review the complete plan or error output.
5. Check resource references, provider versions, and IAM dependencies.

**Recovery**
- Fix the specific configuration error.
- Re-run formatting, initialization, validation, and planning.
- Review all proposed changes before any deployment.

Never run `terraform apply` solely to test whether a configuration works.

### 7. Remediation Safety Failure

**Symptoms**
- A remediation is rejected.
- Retry limits are reached.
- A high-risk action requires approval.

**Diagnosis**
1. Inspect the incident type and remediation mapping.
2. Verify the approval flag for high-risk actions.
3. Review retry count and previous action results.
4. Check whether the incident is already resolved or failed.

**Recovery**
- Obtain explicit approval when required.
- Do not bypass retry