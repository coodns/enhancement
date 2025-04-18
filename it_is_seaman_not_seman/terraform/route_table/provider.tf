terraform {
  backend "remote" {
    organization = "enhancement"

    workspaces {
      name = "route_table"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-2"
}