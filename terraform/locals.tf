locals {
  app_name          = "fastapi-starter"
  environment       = var.ENVIRONMENT
  domain_name       = "api.nextonlabs.com"
  health_check_path = "/docs"
  split_domain      = split(".", local.domain_name)
  hosted_zone_name  = "${join(".", slice(local.split_domain, 1, length(local.split_domain)))}"
  bucket_name       = local.app_name
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
        value : module.s3-bucket.s3_bucket_name
      },
      {
        name : "COGNITO_POOL_ID",
        value : module.auth.user_pool_id
      },
      {
        name : "COGNITO_REGION",
        value : data.aws_region.current.id
    }]
    "logConfiguration" = {
      "logDriver" = "awslogs",
      "options" = {
        "awslogs-group"         = module.logs.log_group_name,
        "awslogs-region"        = data.aws_region.current.id,
        "awslogs-stream-prefix" = "ecs"
      }
    }
  })
}