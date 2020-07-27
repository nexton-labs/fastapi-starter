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
  container_definition = jsonencode({
    "name"        = "${local.app_name}-${local.environment}"
    "image"       = "${data.aws_ecr_repository.repository.repository_url}:${var.IMAGE_TAG}"
    "essential"   = true
    "networkMode" = "awsvpc"
    "portMappings" = [{
      hostPort      = 80,
      protocol      = "tcp",
      containerPort = 80
    }]
    "logConfiguration" = {
      "logDriver" = "awslogs",
      "options" = {
        "awslogs-group"         = module.logs.log_group_name,
        "awslogs-region"        = local.default_region,
        "awslogs-stream-prefix" = "ecs"
      }
    }
  })
}