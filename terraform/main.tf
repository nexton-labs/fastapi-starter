module "logs" {
  source            = "git@github.com:nexton-labs/infrastructure.git//modules/aws/cloudwatch"
  app_name          = local.app_name
  environment       = local.environment
  resource          = "ecs"
  retention_in_days = 7
}

module "cluster" {
  source      = "git@github.com:nexton-labs/infrastructure.git//modules/aws/ecs"
  app_name    = local.app_name
  environment = local.environment
}

module "ecs-lb" {
  source          = "git@github.com:nexton-labs/infrastructure.git//modules/aws/lb/standard"
  name            = local.app_name
  environment     = local.environment
  vpc_id          = local.vpc_id
  subnet_ids      = local.subnet_ids
  internal        = false
  target_type     = "ip"
  certificate_arn = data.aws_acm_certificate.main.arn
  health_check = {
    enabled             = true
    interval            = 30
    port                = 80
    protocol            = "HTTP"
    path                = local.health_check_path
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200"
  }
  module_depends_on = [data.aws_security_group.allow_http_from_everywhere]
}

module "s3-bucket" {
  source             = "git@github.com:nexton-labs/infrastructure.git//modules/aws/s3"
  name               = local.bucket_name
  app_name           = local.app_name
  environment        = local.environment
  acl                = "private"
  versioning_enabled = false
  sse_algorithm      = "aws:kms"
}

resource "aws_db_subnet_group" "default" {
  name       = "dev-internal"
  subnet_ids = local.subnet_ids
}

# per-app database below
module "rds_parameters" {
  source       = "git@github.com:nexton-labs/infrastructure.git//modules/aws/rds/parameter_groups/aurora-postgresql/11.7/default"
  cluster_name = local.rds_cluster_name
}

module "fastapi_rds" {
  source                        = "git@github.com:nexton-labs/infrastructure.git//modules/aws/rds/aurora"
  cluster_name                  = local.rds_cluster_name
  cluster_count                 = 1
  security_group_ids            = [data.aws_security_group.allow_postgresql_from_intranet.id]
  db_subnet_group_name          = aws_db_subnet_group.default.name
  instance_class                = "db.t3.medium"
  apply_immediately             = true
  cluster_parameter_group_name  = module.rds_parameters.cluster_parameter_group_name
  instance_parameter_group_name = module.rds_parameters.instance_parameter_group_name
}

resource "aws_ecs_task_definition" "fastapi-task" {
  family                   = local.app_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  container_definitions    = "[${local.container_definition}]"
  execution_role_arn       = module.cluster.execution_role_arn
}

resource "aws_ecs_service" "fastapi-service" {
  name            = "${local.app_name}-${local.environment}"
  cluster         = module.cluster.id
  launch_type     = "FARGATE"
  task_definition = aws_ecs_task_definition.fastapi-task.arn
  desired_count   = 1
  network_configuration {
    subnets          = local.subnet_ids
    security_groups  = [data.aws_security_group.allow_http_from_everywhere.id, data.aws_security_group.allow_all_to_everywhere.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = module.ecs-lb.target_group_arn
    container_name   = "${local.app_name}-${local.environment}"
    container_port   = 80
  }
  depends_on = [module.ecs-lb, module.auth]
}


module "auth" {
  source = "git@github.com:nexton-labs/infrastructure.git//modules/aws/cognito"

  app_name                 = "fast_api_starter"
  stage                    = "dev"
  region                   = "us-east-1"
  cognito_role_external_id = "fast-api-starter-unique-4567123576"
}