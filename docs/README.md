# Automated Cloud Operations & Self-Healing Platform

## Project Overview

This project demonstrates a simulated cloud-operations workflow that validates infrastructure incidents, classifies severity, tracks incident states, and performs controlled remediation actions.

## Technology Stack

- Python
- AWS Lambda
- Amazon SQS and Dead-Letter Queue
- Amazon DynamoDB
- Amazon S3
- AWS IAM
- Terraform
- pytest
- GitHub Actions

## Architecture

1. A simulated incident is generated as JSON.
2. The incident engine validates required fields and timestamp format.
3. Supported incident types are assigned LOW, MEDIUM, or HIGH severity.
4. The Lambda handler processes SQS-style records and writes incident data to DynamoDB.
5. The remediation engine simulates approved recovery actions, retry limits, and safety controls.
6. Terraform defines the intended cloud infrastructure.

## Local Setup

Create and activate a Python virtual environment, then install the project test dependencies.

Run tests:

```powershell
python -m pytest -v
```

Build the Lambda package:

```powershell
python build_lambda.py
```

Validate Terraform:

```powershell
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
terraform -chdir=terraform plan
```

## Test Results

The local test suite has passed 21 tests in the latest reported run. Terraform validation and a plan proposing 11 resources were also reported successful.

## Security and Cost Notes

- Terraform is used to define infrastructure as code.
- IAM permissions are scoped where practical and should be reviewed before deployment.
- Generated ZIP files, Terraform state, plan files, and environment files are excluded through `.gitignore`.
- Local secret-pattern scans returned no matches for the patterns checked.
- AWS Free Tier does not guarantee zero cost. Check current pricing and account eligibility before deployment.
- Do not run `terraform apply` without reviewing the plan, permissions, and expected charges.

## Limitations

The project has been tested locally with automated tests and mocked AWS dependencies. Actual SQS, Lambda, DynamoDB, CloudWatch, and DLQ integration has not yet been verified in AWS.

GitHub Actions workflow configuration exists locally, but a successful run on GitHub has not yet been confirmed.

## Future Improvements

- Verify end-to-end processing in a controlled AWS environment.
- Test dead-letter queue behavior and recovery.
- Add structured audit records and operational dashboards.
- Complete architecture, IAM permission, and troubleshooting documentation.
