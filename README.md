# AI-Powered Cybersecurity Threat Detection Platform

I built this project to practice bringing AI, cloud engineering, security, and DevOps together in one realistic platform. The goal is to take a trained machine learning model for network threat detection and serve it through a production-style API that can be tested, monitored, containerized, and deployed with cloud infrastructure.

At a high level, the platform accepts network/security feature data, runs it through a scikit-learn model, returns a threat prediction, creates an alert, and gives the analyst a short explanation of what to do next.

Demo screenshots and a walkthrough are available in `docs/demo.md`.

## What This Project Shows

This project is meant to demonstrate more than just model training. It shows the surrounding engineering work needed to make an AI service usable:

- A FastAPI service for real-time model inference
- JWT authentication for protected endpoints
- Threat predictions with risk level, confidence, model version, and recommendations
- Alert generation and alert listing
- A simple analyst explanation endpoint
- Prometheus metrics for monitoring
- Docker support for containerized deployment
- Kubernetes manifests for orchestration
- Terraform infrastructure for AWS ECS Fargate
- GitHub Actions CI/CD for testing, Terraform validation, Docker build, and container publishing

## Tech Stack

The platform uses:

- Python and FastAPI for the API
- scikit-learn for the machine learning model
- Docker and Docker Compose for containerization
- Kubernetes for deployment scaffolding
- Terraform for AWS infrastructure
- AWS ECS Fargate, ECR, ALB, and CloudWatch for the cloud architecture
- Prometheus and Grafana for monitoring
- GitHub Actions for CI/CD

## How It Works

```text
Security data
  |
  v
FastAPI API
  |
  +--> Authenticate request
  |
  +--> Run ML threat prediction
  |
  +--> Generate alert
  |
  +--> Return analyst-friendly response
  |
  +--> Expose metrics for monitoring
  |
  v
Docker / Kubernetes / AWS ECS Fargate
```

## API Endpoints

| Method | Endpoint | What it does |
| --- | --- | --- |
| `GET` | `/` | Confirms the platform is running |
| `GET` | `/health` | Checks API and model health |
| `GET` | `/model-info` | Shows model metadata and expected feature count |
| `POST` | `/login` | Returns a bearer token |
| `POST` | `/predict` | Runs an authenticated threat prediction |
| `GET` | `/alerts` | Lists generated alerts |
| `POST` | `/explain-threat` | Returns simple analyst guidance |
| `GET` | `/metrics` | Exposes Prometheus metrics |

## Running It Locally

Install the project dependencies:

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

For the demo login, use:

```text
username: admin
password: password123
```

After logging in, use `sample_prediction_request.json` as the request body for `/predict`.

## Screenshots And Demo

I added a visual walkthrough in `docs/demo.md` with screenshots of Swagger UI, the health check, model metadata, and a real prediction response.

Demo screenshots:

- `docs/assets/swagger-ui.png`
- `docs/assets/health-endpoint.png`
- `docs/assets/model-info-endpoint.png`
- `docs/assets/prediction-response.png`

There is also a small PowerShell demo script:

```powershell
.\scripts\demo_api.ps1
```

If Windows blocks script execution, run it with a one-time bypass:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_api.ps1
```

If your API is running on another port:

```powershell
.\scripts\demo_api.ps1 -BaseUrl http://127.0.0.1:8010
```

Example response:

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

## CI/CD

The GitHub Actions pipeline runs automatically on pushes and pull requests. It checks both the application and the infrastructure code.

The pipeline:

- Installs Python dependencies
- Compiles the application files
- Runs the API test suite
- Checks Terraform formatting
- Initializes Terraform without a backend
- Validates the Terraform configuration
- Builds the Docker image
- Publishes the container image to GitHub Container Registry on push events

Container image:

```text
ghcr.io/candicetech/ai-threat-detection-platform
```

## AWS Infrastructure

The Terraform code in `terraform/` defines an AWS deployment using ECS Fargate.

It creates:

- A VPC with public subnets
- An Internet Gateway and route table
- An ECR repository for the API image
- An ECS Fargate cluster and service
- An Application Load Balancer
- Security groups
- A CloudWatch log group
- An ECS task execution role

Basic Terraform workflow:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

The Terraform README includes more detail on pushing the Docker image and cleaning up resources.

## Kubernetes

The `kubernetes/` folder includes basic deployment and service manifests for running the API in a Kubernetes cluster.

## Testing

The test suite covers the main platform flow:

- Health checks
- Model metadata
- Login success and failure
- Authenticated prediction
- Feature count validation
- Alert listing
- Threat explanation response

Run tests with:

```bash
pytest -q
```

## What I Learned

This project helped me practice the full path from model artifact to deployable service. I worked through model loading, API design, authentication, test coverage, Docker builds, Terraform infrastructure, and CI/CD.

One useful lesson was debugging a GitHub Actions failure caused by differences between my local Windows environment and GitHub's Linux runner. Fixing that taught me why environment consistency matters in real DevOps and MLOps work.

## How I Would Describe It

> A cloud-native AI threat detection platform that serves a trained cybersecurity model through FastAPI, protects prediction endpoints with authentication, generates alerts and analyst guidance, exposes Prometheus metrics, and includes Docker, Kubernetes, Terraform AWS infrastructure, and GitHub Actions CI/CD.

The strongest parts to discuss are:

- How the ML model is served through an API
- How authentication protects the prediction workflow
- How alerts and recommendations make the raw model output more useful
- How Prometheus metrics support monitoring
- How Docker and Kubernetes prepare the app for deployment
- How Terraform defines the AWS ECS Fargate infrastructure
- How CI/CD validates both the application and infrastructure code

## Future Improvements

Next, I would like to add:

- Persistent alert storage with PostgreSQL or DynamoDB
- A production identity provider instead of demo credentials
- Grafana dashboard JSON files
- LLM-powered threat intelligence enrichment
- Automated model retraining
- A live AWS deployment URL

## Author

Candice Scarborough
