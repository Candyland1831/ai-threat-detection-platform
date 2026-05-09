# Terraform AWS Infrastructure

This Terraform stack deploys the AI Threat Detection API to AWS using ECS Fargate.

## What It Creates

- VPC with two public subnets
- Internet gateway and public route table
- ECR repository for the Docker image
- ECS Fargate cluster, task definition, and service
- Application Load Balancer
- Security groups for the load balancer and API service
- CloudWatch log group for container logs
- IAM task execution role

## Architecture

```text
Internet
  |
  v
Application Load Balancer
  |
  v
ECS Fargate Task
  |
  v
FastAPI AI Threat Detection API
```

## Usage

Copy the example variables file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Initialize Terraform:

```bash
terraform init
```

Preview the infrastructure:

```bash
terraform plan
```

Deploy:

```bash
terraform apply
```

After deployment, Terraform prints `application_url`.

## Container Image Flow

The stack creates an ECR repository. A typical deployment flow is:

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t ai-threat-detection .
docker tag ai-threat-detection:latest <ecr-repository-url>:latest
docker push <ecr-repository-url>:latest
terraform apply
```

## Cleanup

To avoid ongoing AWS charges:

```bash
terraform destroy
```
