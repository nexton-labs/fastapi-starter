# IAM policy document (to allow Lambda to assume a role)
data "aws_iam_policy_document" "lambda-assume-role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# AWS IAM role (to allow Lambda to assume a role)
resource "aws_iam_role" "lambda_role" {
  name               = "${local.app_name}-${local.environment}-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role.json

  tags = {
    Application = local.app_name
    Environment = local.environment
    Service     = "lambda"
  }
}


data "aws_iam_policy_document" "lambda_vpc_policy_document" {
  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "ec2:CreateNetworkInterface",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DeleteNetworkInterface",
      "ec2:AssignPrivateIpAddresses",
      "ec2:UnassignPrivateIpAddresses"
    ]
    resources = [
      "*"
    ]
  }
}

# AWS IAM policy
resource "aws_iam_policy" "lambda_vpc_policy" {
  name   = "${local.app_name}-${local.environment}-lamdaPolicyVPC"
  policy = data.aws_iam_policy_document.lambda_vpc_policy_document.json
}

# Attaches a managed IAM policy to an IAM role
resource "aws_iam_role_policy_attachment" "lambda_role_rds_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_vpc_policy.arn
}

resource "aws_lambda_function" "user_post_confirmation" {
  filename         = "example.zip"
  function_name    = "${local.app_name}-${local.environment}-PostUserConfirmation"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.lambda_handler"
  source_code_hash = filebase64sha256("example.zip")

  runtime = "python3.8"

  vpc_config {
    # Every subnet should be able to reach an EFS mount target in the same Availability Zone. Cross-AZ mounts are not permitted.
    subnet_ids         = tolist(module.vpc.private_subnet_id)
    security_group_ids = [data.aws_security_group.allow_all_to_everywhere.id, data.aws_security_group.allow_all_from_intranet.id]
  }

  environment {
    variables = {
      dbHost     = module.fastapi_rds.writer_endpoint
      dbName     = "postgres"
      dbPort     = module.fastapi_rds.db_port
      dbUser     = split(":", module.fastapi_rds.root_credentials)[0]
      dbPassword = split(":", module.fastapi_rds.root_credentials)[1]
    }
  }

  tags = {
    Application = local.app_name
    Environment = local.environment
  }
}