
resource "aws_iam_role" "incident_lambda" {
  name = "${var.project_name}-lambda-role-${random_id.suffix.hex}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_cloudwatch_log_group" "incident_processor" {
  name = "/aws/lambda/${var.project_name}-processor-${random_id.suffix.hex}"

  retention_in_days = 7
}

resource "aws_iam_role_policy" "incident_lambda" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.incident_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ReadIncidentQueue"
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:ChangeMessageVisibility"
        ]
        Resource = aws_sqs_queue.incident_queue.arn
      },
      {
        Sid    = "WriteIncidentRecords"
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem"
        ]
        Resource = aws_dynamodb_table.incidents.arn
      },
      {
        Sid    = "LambdaBasicLogging"
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "${aws_cloudwatch_log_group.incident_processor.arn}:*"
      }
    ]
  })
}
