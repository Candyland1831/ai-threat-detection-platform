output "ecr_repository_url" {
  description = "ECR repository URL for pushing the API container image."
  value       = aws_ecr_repository.api.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name."
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECS service name."
  value       = aws_ecs_service.api.name
}

output "load_balancer_dns_name" {
  description = "Public DNS name for the application load balancer."
  value       = aws_lb.api.dns_name
}

output "application_url" {
  description = "HTTP URL for the deployed FastAPI service."
  value       = "http://${aws_lb.api.dns_name}"
}
