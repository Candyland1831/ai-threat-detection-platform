# AI-Powered Cybersecurity Threat Detection Platform

A cloud-native machine learning platform for cybersecurity threat detection built with Python, FastAPI, Docker, Kubernetes, Prometheus, Grafana, and GitHub Actions CI/CD.

## Features

- Real-time ML threat prediction API
- JWT-protected prediction, alert, and explanation endpoints
- Model metadata and health check endpoints
- In-memory alert tracking for analyst review
- AI-assisted threat explanation response for analysts
- FastAPI + Swagger/OpenAPI integration
- Docker containerization
- Kubernetes orchestration
- Prometheus metrics instrumentation
- Grafana operational dashboards
- GitHub Actions CI/CD pipeline

## Tech Stack

- Python
- FastAPI
- scikit-learn
- Docker
- Kubernetes
- Prometheus
- Grafana
- GitHub Actions
- Terraform
- AWS ECS/Fargate

## API Endpoints

- `GET /` - platform status
- `GET /health` - service and model health check
- `GET /model-info` - model metadata and expected feature count
- `POST /login` - returns a bearer token
- `POST /predict` - runs authenticated threat prediction
- `GET /alerts` - lists generated alerts
- `POST /explain-threat` - returns analyst-friendly threat guidance
- `GET /metrics` - Prometheus metrics

## Local Demo

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run tests:

```powershell
pytest -q
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Login with:

```text
username: admin
password: password123
```

Use `sample_prediction_request.json` as the request body for `/predict`.

## DevOps CI/CD

The GitHub Actions pipeline validates the platform on every pull request and push to `main` or `master`.

- Installs Python dependencies
- Compiles the FastAPI and model training code
- Runs API smoke tests with `pytest`
- Builds the Docker image
- Publishes the image to GitHub Container Registry on push events

Container image:

```text
ghcr.io/candyland1831/ai-threat-detection-platform
```

## AWS Infrastructure

Terraform infrastructure lives in `terraform/`.

The AWS stack provisions:

- VPC with public subnets
- ECR repository for the API container image
- ECS Fargate cluster and service
- Application Load Balancer
- Security groups
- CloudWatch logs
- IAM task execution role

Basic commands:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

See `terraform/README.md` for the deployment flow and cleanup steps.

## Architecture

```text
Client Requests
  |
  v
FastAPI ML API
  |
  v
ML Threat Detection Model
  |
  v
Alert and Explanation API
  |
  v
Prometheus Metrics
  |
  v
Grafana Dashboards
```

## Interview Summary

This project demonstrates a cloud-native AI security platform. It trains and serves a cybersecurity threat detection model, protects inference with authentication, generates analyst-friendly alert responses, exposes Prometheus metrics, containerizes the application with Docker, provides Kubernetes and Terraform AWS infrastructure, and validates changes with GitHub Actions CI/CD.

## Future Enhancements

- Persistent alert storage with PostgreSQL or DynamoDB
- LLM-powered threat intelligence enrichment
- Advanced threat analytics dashboards
- Automated retraining workflows

## Author

Candice Scarborough
