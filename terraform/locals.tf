locals {
  app_name          = "fastapi-starter"
  environment       = "dev"
  subnet_ids        = slice(sort(tolist(data.aws_subnet_ids.main.ids)), 3, 5)
  domain_name       = "api.nextonlabs.com"
  health_check_path = "/docs"
  split_domain      = split(".", local.domain_name)
  hosted_zone_name  = "${join(".", slice(local.split_domain, 1, length(local.split_domain)))}"
  vpc_id            = "vpc-2b933151"
  default_region    = "us-east-1"
}