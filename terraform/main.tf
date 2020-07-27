module "security-groups" {
  source = "git@github.com:nexton-labs/infrastructure.git//modules/aws/vpc/security_groups"

  vpc_id = local.vpc_id
}

module "logs" {
  source = "git@github.com:nexton-labs/infrastructure.git//modules/aws/cloudwatch"

  app_name          = local.app_name
  environment       = local.environment
  resource          = "ecs"
  retention_in_days = 7
}

module "repository" {
  source = "git@github.com:nexton-labs/infrastructure.git//modules/aws/ecr"

  app_name    = local.app_name
  environment = local.environment
}

module "cluster" {
  source = "git@github.com:nexton-labs/infrastructure.git//modules/aws/ecs"

  app_name    = local.app_name
  environment = local.environment
}

module "ecs-lb" {
  source = "git@github.com:nexton-labs/infrastructure.git//modules/aws/lb/standard"

  name        = local.app_name
  environment = local.environment

  vpc_id      = local.vpc_id
  subnet_ids  = local.subnet_ids
  internal    = false
  target_type = "ip"

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
}

resource "aws_ecs_task_definition" "fastapi-task" {
  family                   = local.app_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  container_definitions    = data.template_file.task_definition_tpl.rendered
  execution_role_arn       = module.cluster.execution_role_arn
}

resource "aws_ecs_service" "fastapi-service" {
  name            = "${local.app_name}-${local.environment}"
  cluster         = module.cluster.id
  launch_type     = "FARGATE"
  task_definition = aws_ecs_task_definition.fastapi-task.arn
  desired_count   = 2

  network_configuration {
    subnets         = local.subnet_ids
    security_groups = module.ecs-lb.security_groups
  }

  load_balancer {
    target_group_arn = module.ecs-lb.target_group_arn
    container_name   = "${local.app_name}-${local.environment}"
    container_port   = 80
  }

  depends_on = [module.ecs-lb]
}


