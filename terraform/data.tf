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

data "aws_security_group" "allow_postgresql_from_intranet" {
  name = "allow_postgresql_from_intranet"
}

data "aws_security_group" "allow_http_from_everywhere" {
  name = "allow_http_from_everywhere"
}
data "aws_security_group" "allow_all_to_everywhere" {
  name = "allow_all_to_everywhere"
}