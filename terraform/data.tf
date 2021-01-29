data "aws_region" "current" {}

data "aws_ecr_repository" "repository" {
  name = "${local.app_name}-${local.environment}"
}

data "aws_route53_zone" "main" {
  name = local.hosted_zone_name
}

data "aws_acm_certificate" "main" {
  domain      = local.hosted_zone_name
  types       = ["AMAZON_ISSUED"]
  most_recent = true
}

data "aws_security_group" "allow_postgresql_from_intranet" {
  name   = "allow_postgresql_from_intranet"
  vpc_id = module.vpc.vpc_id

  depends_on = [module.security-groups]
}

data "aws_security_group" "allow_http_from_everywhere" {
  name   = "allow_http_from_everywhere"
  vpc_id = module.vpc.vpc_id

  depends_on = [module.security-groups]
}

data "aws_security_group" "allow_all_to_everywhere" {
  name   = "allow_all_to_everywhere"
  vpc_id = module.vpc.vpc_id

  depends_on = [module.security-groups]
}

data "aws_security_group" "allow_all_from_intranet" {
  name   = "allow_all_from_intranet"
  vpc_id = module.vpc.vpc_id

  depends_on = [module.security-groups]
}