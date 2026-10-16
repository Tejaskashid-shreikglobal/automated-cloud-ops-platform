
output "incident_bucket_name" {
  value = aws_s3_bucket.incident_evidence.bucket
}

output "incident_queue_url" {
  value = aws_sqs_queue.incident_queue.url
}

output "incident_dlq_url" {
  value = aws_sqs_queue.incident_dlq.url
}

output "incident_table_name" {
  value = aws_dynamodb_table.incidents.name
}

output "lambda_execution_role_arn" {
  value = aws_iam_role.incident_lambda.arn
}
