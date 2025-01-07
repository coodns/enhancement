module "atlantis" {
  source  = "terraform-aws-modules/atlantis/aws"

  name = "atlantis"

  create_certificate = false
  certificate_arn = "<ACM ARN>"
  create_route53_records      = false

  # ECS Container Definition
  atlantis = {
    environment = [
      {
        name  = "ATLANTIS_GH_USER"
        value = "<Gitlab Atlantis User>"
      },
      {
        name  = "ATLANTIS_REPO_ALLOWLIST"
        value = "<gitlab allowlist>"
      },
    ]
    secrets = [
      {
        name      = "ATLANTIS_GITLAB_TOKEN"
        valueFrom = "<Gitlab Atlantis Access Token>"
      },
      {
        name      = "ATLANTIS_GITLAB_WEBHOOK_SECRET"
        valueFrom = "<Secret Token For Webhook Secret>"
      },
    ]
  }

  # ECS Service
  service = {
    task_exec_secret_arns = [
      "this is the aws secret manager arn",
      "it contains contianer definition's secret",
    ]
    # Provide Atlantis permission necessary to create/destroy resources
    tasks_iam_role_policies = {
      AdministratorAccess = "arn:aws:iam::aws:policy/AdministratorAccess"
    }
  }
  service_subnets = "insert where you want to place to ecs services"
  vpc_id          = "insert where you want to place to ecs services"

  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}