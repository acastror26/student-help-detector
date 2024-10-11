# FastAPI Hexagonal Architecture Application

### Prerequisites

- Docker
- Docker Compose
- Terraform (for deployment)

### How to Run the Project Locally

Build and run the application:

```bash
docker-compose up --build
```
The application will be available at http://localhost:8000. Kibana will be available at http://localhost:5601.

### Apply migrations:

```bash
docker-compose exec fastapi alembic upgrade head
```
The database, Elasticsearch, and Logstash will be automatically configured.

### Terraform Deployment
```bash
cd terraform
terraform init
terraform apply
```