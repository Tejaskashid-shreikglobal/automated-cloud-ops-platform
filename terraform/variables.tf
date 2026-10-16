
variable "aws_region" {
  description = "AWS region for project resources"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "automated-cloud-ops"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
