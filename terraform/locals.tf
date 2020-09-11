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
  bucket_name       = "fastapi-starter"
  rds_cluster_name  = "fastapi-db-${local.environment}"
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
    "environment" : [
      {
        name : "DATABASE_URL",
        value : "postgresql://${module.fastapi_rds.root_credentials}@${module.fastapi_rds.writer_endpoint}:${module.fastapi_rds.db_port}/postgres"
      },
      {
        name : "AWS_IMG_BUCKET",
        value : "${local.bucket_name}-${local.environment}"
      },
      {
        name : "COGNITO_POOL_ID",
        value : module.auth.identity_pool_id
      },
      {
        name : "COGNITO_REGION",
        value : local.default_region
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