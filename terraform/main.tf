module "vpc" {
  source      = "git@github.com:nexton-labs/infrastructure.git//modules/aws/vpc/vpc"
  app_name    = local.app_name
  environment = local.environment
}

module "security-groups" {
  source = "git@github.com:nexton-labs/infrastructure.git//modules/aws/vpc/security_groups"

  vpc_id      = module.vpc.vpc_id
  app_name    = local.app_name
  environment = local.environment
  groups      = ["HTTP", "PostgreSQL"]
}

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
  app_name        = local.app_name
  environment     = local.environment
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = tolist(module.vpc.public_subnet_id)
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
  name       = "${local.environment}-internal"
  subnet_ids = tolist(module.vpc.private_subnet_id)
}

# per-app database below
module "rds_parameters" {
  source      = "git@github.com:nexton-labs/infrastructure.git//modules/aws/rds/parameter_groups/aurora-postgresql/11.7/default"
  app_name    = local.app_name
  environment = local.environment
}

module "fastapi_rds" {
  source                        = "git@github.com:nexton-labs/infrastructure.git//modules/aws/rds/aurora"
  cluster_count                 = 1
  security_group_ids            = [data.aws_security_group.allow_postgresql_from_intranet.id]
  db_subnet_group_name          = aws_db_subnet_group.default.name
  instance_class                = "db.t3.medium"
  apply_immediately             = true
  cluster_parameter_group_name  = module.rds_parameters.cluster_parameter_group_name
  instance_parameter_group_name = module.rds_parameters.instance_parameter_group_name
  app_name                      = local.app_name
  environment                   = local.environment
}

module "auth" {
  source = "git@github.com:nexton-labs/infrastructure.git//modules/aws/cognito"

  app_name                     = local.app_name
  environment                  = local.environment
  cognito_role_external_id     = "cognito_role_external_id"
  enabled_providers            = ["Google", "Facebook"]
  callback_urls                = ["https://www.nextonlabs.com"]
  enable_mfa                   = true
  mfa_methods                  = ["TOTP", "SMS"]
  google_client_id             = var.GOOGLE_CLIENT_ID
  google_client_secret         = var.GOOGLE_CLIENT_SECRET_ID
  facebook_client_id           = var.FACEBOOK_CLIENT_ID
  facebook_client_secret       = var.FACEBOOK_CLIENT_SECRET_ID
  post_confirmation_lambda_arn = aws_lambda_function.user_post_confirmation.arn
}

# IAM policy document (to allow ECS tasks to assume a role)
data "aws_iam_policy_document" "task-assume-role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# AWS IAM role (to allow ECS tasks to assume a role)
resource "aws_iam_role" "ecs_task_role" {
  name               = "${local.app_name}-${local.environment}-ecsTaskRole"
  assume_role_policy = data.aws_iam_policy_document.task-assume-role.json

  tags = {
    Application = local.app_name
    Environment = local.environment
    Service     = "ecs"
  }
}

# [Data] IAM policy to define S3 permissions
data "aws_iam_policy_document" "s3_data_bucket_policy" {
  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::${module.s3-bucket.s3_bucket_name}"
    ]
  }
  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "s3:DeleteObject",
      "s3:GetObject",
      "s3:PutObject",
      "s3:PutObjectAcl"
    ]
    resources = [
      "arn:aws:s3:::${module.s3-bucket.s3_bucket_name}/*"
    ]
  }
}

# AWS IAM policy
resource "aws_iam_policy" "s3_policy" {
  name   = "${local.app_name}-${local.environment}-taskPolicyS3"
  policy = data.aws_iam_policy_document.s3_data_bucket_policy.json

  depends_on = [module.s3-bucket]
}

# Attaches a managed IAM policy to an IAM role
resource "aws_iam_role_policy_attachment" "ecs_role_s3_data_bucket_policy_attach" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}

# [Data] IAM policy to define cognito permissions
data "aws_iam_policy_document" "cognito_idp_policy" {
  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "cognito-idp:*"
    ]
    resources = [
      module.auth.arn
    ]
  }
}

# AWS IAM cognito policy
resource "aws_iam_policy" "cognito_policy" {
  name   = "${local.app_name}-${local.environment}-taskPolicyCognito"
  policy = data.aws_iam_policy_document.cognito_idp_policy.json
}

# Attaches a managed IAM cognito policy to an IAM role
resource "aws_iam_role_policy_attachment" "ecs_role_cognito_idp_policy_attach" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.cognito_policy.arn
}

resource "aws_ecs_task_definition" "fastapi-task" {
  family                   = local.app_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  container_definitions    = "[${local.container_definition}]"
  execution_role_arn       = module.cluster.execution_role_arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
}

resource "aws_ecs_service" "fastapi-service" {
  name            = "${local.app_name}-${local.environment}"
  cluster         = module.cluster.id
  launch_type     = "FARGATE"
  task_definition = aws_ecs_task_definition.fastapi-task.arn
  desired_count   = 1
  network_configuration {
    subnets          = tolist(module.vpc.public_subnet_id)
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

resource "aws_route53_record" "route53" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "${local.domain_name}."
  type    = "A"

  alias {
    name                   = module.ecs-lb.dns_name
    zone_id                = module.ecs-lb.zone_id
    evaluate_target_health = false
  }
}
