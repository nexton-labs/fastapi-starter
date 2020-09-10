variable "IMAGE_TAG" {
}

variable "AWS_ACCESS_KEY_ID" {
  type        = string
  description = "AWS access key ID (set from terraform cloud)"
}

variable "AWS_SECRET_ACCESS_KEY" {
  type        = string
  description = "AWS secret access key (set from terraform cloud)"
}