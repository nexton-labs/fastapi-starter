[
      {
          "name": "fastapi-starter",
          "image": "${REPOSITORY_URL}:${TAG}",
          "networkMode": "awsvpc",
          "essential": true,
          "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
              "awslogs-group": "${LOGS_GROUP}",
              "awslogs-region": "${AWS_ECR_REGION}",
              "awslogs-stream-prefix": "ecs"
            }
          }
          "portMappings": [
            {
              "hostPort": 80,
              "protocol": "tcp",
              "containerPort": 80
            }
          ]
      }
  ]