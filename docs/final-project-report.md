# Automated Cloud Operations & Self-Healing Platform

## 1. Project Overview

This project implements a prototype platform for automated cloud incident processing and simulated self-healing operations. It uses Python for incident validation and remediation logic, Terraform for AWS infrastructure definitions, and GitHub Actions for continuous integration.

**Deployment status:** Local prototype and infrastructure validation completed. AWS resources have not been deployed.

## 2. Objectives

- Validate incoming incident events.
- Classify incidents by severity.
- Track incident states and transitions.
- Simulate remediation actions with approval and retry controls.
- Define AWS infrastructure using Terraform.
- Validate code through automated tests and GitHub Actions.

## 3. Architecture

Incident Event / JSON
-> Amazon SQS incident queue
-> AWS Lambda incident processor
-> Amazon DynamoDB incident records

Supporting components:
- Amazon SQS dead-letter queue for messages that repeatedly fail processing.
- Amazon S3 bucket configuration for incident evidence.
- Amazon CloudWatch log group with seven-day retention.
- AWS IAM role and scoped permissions.
- Terraform for infrastructure provisioning.
- GitHub Actions for Python tests and Terraform validation.

The AWS architecture is defined in code; live AWS integration has not been verified.

## 4. Technology Stack

- Python 3.11 for local development and tests.
- pytest for automated testing.
- boto3 for AWS SDK integration.
- Terraform for infrastructure as code.
- AWS Lambda, SQS, DynamoDB, S3, CloudWatch and IAM in the planned architecture.
- Git and GitHub Actions for source control and CI.

## 5. Incident Processing and Remediation

The prototype validates required incident fields and classifies supported incident types:

- `service_unhealthy` â€” HIGH
- `config_drift` â€” MEDIUM
- `temp_backlog` â€” LOW

The local remediation engine simulates supported actions, enforces approval for configuration restoration, limits retries, and avoids repeating a successful remediation.

## 6. Testing and Validation

- Python test suite: 29 tests passed locally.
- Lambda handler tests: 5 tests passed.
- Terraform formatting check: completed without reported formatting errors.
- Terraform validation: successful.
- Terraform plan: 11 resources to add, 0 to change, 0 to destroy.
- GitHub Actions: latest workflow run displayed a successful status.

### Latest CI Verification

- Python test suite: 30 tests passed locally.
- GitHub Actions: Project CI workflow run #15 completed successfully.
- Terraform formatting and validation: passed in CI.
- Lambda deployment package: built as part of the CI workflow before Terraform validation.
- AWS deployment: not performed; validation was limited to local checks and CI.


These results verify local tests and configuration checks. They do not prove that AWS resources were deployed or that live AWS event processing works end to end.

## 7. Security and Cost Considerations

- S3 public access is blocked in the Terraform configuration.
- S3 server-side encryption and versioning are configured.
- DynamoDB uses on-demand billing in the planned infrastructure.
- IAM permissions are scoped to the resources and actions required by the prototype.
- CloudWatch log retention is set to seven days.
- No AWS deployment was performed as part of this validation, avoiding deployment-related charges during development.

A real deployment would require review of IAM policies, costs, monitoring, secrets handling, and operational procedures.

## 8. Limitations

- AWS Lambda, SQS and DynamoDB integration has not been tested in a deployed AWS environment.
- Remediation actions are simulations, not real server operations.
- Persistent audit storage and live CloudWatch alarms have not been verified end to end.
- The Terraform plan represents proposed infrastructure changes only.

## 9. Future Enhancements

- Deploy in a controlled AWS test account after reviewing cost and permissions.
- Test SQS-to-Lambda processing and DynamoDB persistence.
- Add CloudWatch alarms and validate dead-letter queue behavior.
- Implement durable remediation audit records and operational dashboards.
- Add integration tests using mocked AWS services or a local AWS-compatible test environment.

## 10. Conclusion

The project demonstrates a tested local incident-processing prototype, simulated self-healing logic, infrastructure-as-code definitions, and CI validation. The local Python suite passed all 29 tests, Terraform validation succeeded, and the latest GitHub Actions run showed success. Live AWS deployment and end-to-end cloud behavior remain future validation steps.
