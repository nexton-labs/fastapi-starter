data "aws_vpc" "main" {
  id = local.vpc_id
}

data "aws_subnet_ids" "main" {
  vpc_id = data.aws_vpc.main.id
}

data "aws_region" "current" {}

data "aws_acm_certificate" "main" {
  domain      = local.hosted_zone_name
  types       = ["AMAZON_ISSUED"]
  most_recent = true
}

data "aws_ecr_repository" "repository" {
  name = "${local.app_name}-${local.environment}"
}

data "template_file" "task_definition_tpl" {
  template = file("task-template.json.tpl")
  vars = {
    REPOSITORY_URL = data.repository.repository_url
    TAG            = var.image_tag
    AWS_ECR_REGION = local.default_region
    LOGS_GROUP     = module.logs.log_group_name
  }
}