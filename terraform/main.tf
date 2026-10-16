
resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "incident_evidence" {
  bucket = "${var.project_name}-${random_id.suffix.hex}"

  force_destroy = false
}

resource "aws_sqs_queue" "incident_dlq" {
  name                      = "${var.project_name}-dlq-${random_id.suffix.hex}"
  message_retention_seconds = 1209600
}

resource "aws_sqs_queue" "incident_queue" {
  name                       = "${var.project_name}-queue-${random_id.suffix.hex}"
  visibility_timeout_seconds = 180
  message_retention_seconds  = 345600

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.incident_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_dynamodb_table" "incidents" {
  name         = "${var.project_name}-incidents-${random_id.suffix.hex}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "incident_id"

  attribute {
    name = "incident_id"
    type = "S"
  }
}

resource "aws_s3_bucket_public_access_block" "incident_evidence" {
  bucket = aws_s3_bucket.incident_evidence.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "incident_evidence" {
  bucket = aws_s3_bucket.incident_evidence.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "incident_evidence" {
  bucket = aws_s3_bucket.incident_evidence.id

  versioning_configuration {
    status = "Enabled"
  }
}
resource "aws_lambda_function" "incident_processor" {
  function_name = "${var.project_name}-processor-${random_id.suffix.hex}"
  role          = aws_iam_role.incident_lambda.arn

  runtime = "python3.12"
  handler = "lambda_handler.lambda_handler"

  filename         = "${path.module}/lambda_package.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda_package.zip")

  timeout     = 30
  memory_size = 128

  environment {
    variables = {
      INCIDENT_TABLE = aws_dynamodb_table.incidents.name
      AWS_REGION     = var.aws_region
    }
  }

  depends_on = [
    aws_iam_role_policy.incident_lambda,
    aws_cloudwatch_log_group.incident_processor
  ]
}

resource "aws_lambda_event_source_mapping" "incident_queue" {
  event_source_arn = aws_sqs_queue.incident_queue.arn
  function_name    = aws_lambda_function.incident_processor.arn

  batch_size = 1
  enabled    = true
}