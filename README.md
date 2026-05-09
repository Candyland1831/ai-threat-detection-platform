# AI-Powered Cybersecurity Threat Detection Platform

A cloud-native AI security platform that serves a machine learning threat detection model through a FastAPI API. The platform includes authentication, alert generation, analyst-friendly threat explanations, Prometheus metrics, Docker containerization, Kubernetes manifests, Terraform AWS infrastructure, and GitHub Actions CI/CD.

## Project Highlights

- Machine learning inference API for cybersecurity threat detection
- JWT-protected endpoints for prediction, alerts, and explanations
- Model health and metadata endpoints
- Alert generation with risk level, confidence, model version, and recommendation
- Analyst-friendly threat explanation endpoint
- Prometheus-compatible `/metrics` endpoint
- Docker and Docker Compose support
- Kubernetes deployment and service manifests
- Terraform AWS infrastructure for ECS Fargate
- GitHub Actions pipeline for tests, Terraform validation, Docker build, and container publishing

## Tech Stack

- Python
- FastAPI
- scikit-learn
- Docker
- Docker Compose
- Kubernetes
- Terraform
- AWS ECS Fargate
- AWS ECR
- AWS Application Load Balancer
- AWS CloudWatch
- Prometheus
- Grafana
- GitHub Actions

## Architecture

```text
Client / Security Analyst
  |
  v
FastAPI Application
  |
  +--> JWT Authentication
  |
  +--> ML Threat Detection Model
  |
  +--> Alert Generation
  |
  +--> Threat Explanation API
  |
  +--> Prometheus Metrics
  |
  v
Docker / Kubernetes / AWS ECS Fargate
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Platform status |
| `GET` | `/health` | API and model health check |
| `GET` | `/model-info` | Model metadata and expected feature count |
| `POST` | `/login` | Returns a bearer token |
| `POST` | `/predict` | Runs authenticated threat prediction |
| `GET` | `/alerts` | Lists generated alerts |
| `POST` | `/explain-threat` | Returns analyst-friendly threat guidance |
| `GET` | `/metrics` | Prometheus metrics |

## Local Demo

Clone the repository and install dependencies:

```powershell
pip install -r requirements.txt
```

Run the tests:

```powershell
pytest -q
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Login credentials for the demo:

```text
username: admin
password: password123
```

Use `sample_prediction_request.json` as the request body for `/predict`.

Example prediction response:

```json
{
  "alert_id": "generated-alert-id",
  "prediction": 0,
  "threat_status": "normal_activity",
  "risk_level": "LOW",
  "confidence": 0.86,
  "model_version": "security-random-forest-v1",
  "requested_by": "admin",
  "recommendation": "No immediate action required. Continue monitoring for repeated or correlated activity."
}
```

## Docker

Build the image:

```bash
docker build -t ai-threat-detection-platform .
```

Run the container:

```bash
docker run -p 8000:8000 ai-threat-detection-platform
```

## DevOps CI/CD

The GitHub Actions workflow runs on pull requests and pushes to `main` or `master`.

Pipeline jobs:

- Install Python dependencies
- Compile FastAPI and model training files
- Run API tests with `pytest`
- Check Terraform formatting
- Run `terraform init -backend=false`
- Run `terraform validate`
- Build the Docker image
- Publish the image to GitHub Container Registry on push events

Container image:

```text
ghcr.io/candyland1831/ai-threat-detection-platform
```

## AWS Infrastructure

Terraform infrastructure is located in `terraform/`.

The AWS stack provisions:

- VPC with public subnets
- Internet Gateway and route table
- ECR repository for the API container image
- ECS Fargate cluster, task definition, and service
- Application Load Balancer
- Security groups
- CloudWatch log group
- IAM ECS task execution role

Basic Terraform commands:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

See `terraform/README.md` for image push steps and cleanup instructions.

## Kubernetes

Kubernetes manifests are located in `kubernetes/`.

- `deployment.yaml` defines the FastAPI application deployment
- `service.yaml` exposes the API service

## Testing

The test suite validates:

- Health endpoint
- Model metadata endpoint
- Login success and failure
- Authenticated prediction flow
- Feature count validation
- Alert listing
- Threat explanation response

Run tests:

```bash
pytest -q
```

## Interview Summary

This project demonstrates a cloud-native AI security platform. It combines machine learning inference, API development, authentication, observability, containerization, infrastructure as code, and CI/CD.

Strong interview talking points:

- Served a trained cybersecurity ML model with FastAPI
- Added JWT authentication around sensitive inference endpoints
- Generated alert objects with risk level, confidence, and recommendations
- Exposed Prometheus metrics for service monitoring
- Containerized the platform with Docker
- Added Kubernetes deployment scaffolding
- Built AWS ECS Fargate infrastructure with Terraform
- Added CI/CD that validates both application code and Terraform infrastructure
- Debugged CI failures caused by differences between local Windows and GitHub Linux runners

## Future Enhancements

- Store alerts in PostgreSQL or DynamoDB
- Add a production identity provider instead of demo credentials
- Add LLM-powered threat intelligence enrichment
- Add Grafana dashboard JSON files
- Add automated model retraining workflow
- Deploy the Terraform stack to AWS and document the live URL

## Author

Candice Scarborough
