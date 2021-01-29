locals {
  proxy_name = "imgproxy-${local.app_name}"
  imgproxy_container_definition = jsonencode({
    "name"        = "${local.proxy_name}-${local.environment}"
    "image"       = "darthsim/imgproxy:latest"
    "essential"   = true
    "networkMode" = "awsvpc"
    "cpu"         = 0
    "mountPoints" = []
    "volumesFrom" = []
    "portMappings" = [{
      hostPort      = 80,
      protocol      = "tcp",
      containerPort = 80
    }]
    "environment" : [
      {
        name : "IMGPROXY_BIND",
        value : ":80"
      },
      {
        name : "IMGPROXY_USE_S3",
        value : "true"
      },
      {
        name : "IMGPROXY_KEY",
        value : var.IMGPROXY_KEY
      },
      {
        name : "IMGPROXY_SALT",
        value : var.IMGPROXY_SALT
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

module "ecs-imgproxy-lb" {
  source            = "git@github.com:nexton-labs/infrastructure.git//modules/aws/lb/standard"
  app_name          = local.proxy_name
  environment       = local.environment
  vpc_id            = module.vpc.vpc_id
  subnet_ids        = tolist(module.vpc.public_subnet_id)
  internal          = false
  target_type       = "ip"
  certificate_arn   = data.aws_acm_certificate.main.arn
  redirect_to_https = false
  health_check = {
    enabled             = true
    interval            = 30
    port                = 80
    protocol            = "HTTP"
    path                = "/health"
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200"
  }

  module_depends_on = [data.aws_security_group.allow_http_from_everywhere]
}

resource "aws_ecs_task_definition" "imgproxy-task" {
  family                   = local.proxy_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  container_definitions    = "[${local.imgproxy_container_definition}]"
  execution_role_arn       = module.cluster.execution_role_arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
}

resource "aws_ecs_service" "imgproxy-service" {
  name            = "${local.proxy_name}-${local.environment}"
  cluster         = module.cluster.id
  launch_type     = "FARGATE"
  task_definition = aws_ecs_task_definition.imgproxy-task.arn
  desired_count   = 1
  network_configuration {
    subnets          = tolist(module.vpc.public_subnet_id)
    security_groups  = [data.aws_security_group.allow_http_from_everywhere.id, data.aws_security_group.allow_all_to_everywhere.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = module.ecs-imgproxy-lb.target_group_arn
    container_name   = "${local.proxy_name}-${local.environment}"
    container_port   = 80
  }
  depends_on = [module.ecs-imgproxy-lb, module.auth]
}

resource "aws_cloudfront_distribution" "imgproxy-cf-distribution" {
  comment = "${local.proxy_name}-${local.environment}"
  //  aliases          = [local.domain_name]
  enabled = true

  origin {
    domain_name = module.ecs-imgproxy-lb.dns_name
    origin_id   = "ELB-${local.proxy_name}-${local.environment}"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2", "SSLv3"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "ELB-${local.proxy_name}-${local.environment}"

    forwarded_values {
      query_string = true

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 1
    default_ttl            = 86400
    max_ttl                = 31536000
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Application = local.app_name
    Environment = local.environment
  }
}