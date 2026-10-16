# Architecture Diagram

```text
Incident JSON
     |
     v
 Amazon SQS
     |
     v
 AWS Lambda ------> CloudWatch Logs
     |
     v
 Amazon DynamoDB

Supporting tools:
- Terraform
- GitHub Actions
- Local Remediation Engine
```

**Note:** This diagram represents the planned architecture. AWS deployment has not been performed.