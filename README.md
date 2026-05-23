# DevOps Manager

DevOps management platform for deployments, CI/CD, and infrastructure orchestration.

## 🚀 Features

- **Application Management**: Manage your applications and their versions.
- **Deployment Orchestration**: Handle deployments across different environments.
- **CI/CD Pipelines**: Define and monitor automated pipelines.
- **Kubernetes Integration**: Direct interaction with K8s clusters for deployment and monitoring.
- **Real-time Metrics**: Integrated Prometheus metrics for system health.
- **Asynchronous Tasks**: Celery worker for long-running deployment tasks.
- **WebSocket Support**: Real-time updates for deployment logs and status.

## 🛠 Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL (via SQLAlchemy & asyncpg)
- **Task Queue**: Celery & Redis
- **Infrastructure**: Kubernetes, Docker, Nginx
- **Security**: JWT Authentication (python-jose, passlib)
- **Monitoring**: Prometheus

## 📂 Project Structure

```
├── app/
│   ├── api/            # API endpoints (v1)
│   ├── core/           # Configuration, security, and global managers
│   ├── models/         # Database models
│   ├── repositories/    # Data access layer
│   ├── schemas/        # Pydantic validation schemas
│   ├── services/       # Business logic (K8s, Deploy, Pipeline)
│   └── worker/         # Celery worker and background tasks
├── k8s/                # Kubernetes manifests (Deployment, Service, Ingress, etc.)
├── Dockerfile          # Containerization
├── docker-compose.yml  # Local development orchestration
└── pyproject.toml      # Poetry dependency management
```

## ⚙️ Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Poetry (optional, for local development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd devops-manager
   ```

2. **Install dependencies**
   ```bash
   pip install poetry
   poetry install
   ```

3. **Environment Setup**
   Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

### Running Locally (without Docker)

- **Start the API server**:
  ```bash
  poetry run run-server
  ```
- **Start the Celery worker**:
  ```bash
  poetry run run-worker
  ```

## 🧪 Testing

Run tests using pytest:
```bash
poetry run pytest
```

## 📜 License

This project is licensed under the MIT License.
