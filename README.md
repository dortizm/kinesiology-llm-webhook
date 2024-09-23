
# Django Project Kinesiology LLM Webhook with Docker

This is a Django-based project configured to run with Docker. It includes multiple services such as Django application, PostgreSQL, Redis, Celery, and Nginx for a complete development and production environment.

## Prerequisites

Ensure you have the following installed on your local machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

- **web**: Contains the Django application.
- **db**: PostgreSQL database service.
- **redis**: Redis service for caching and message brokering.
- **celery_worker**: Celery worker service for background tasks.
- **celery_beat**: Celery Beat service for scheduled tasks.
- **flower**: Flower service for monitoring Celery workers.
- **nginx**: Nginx service for serving static files and reverse proxy.

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dortizm/kinesiology-llm-webhook
   cd kinesiology-llm-webhook
   ```

2. **Create a `.env` file for environment variables:**

   Copy the example environment file to configure the environment variables:

   ```bash
   cp ./env/.dev-sample ./env/.env
   ```

   Modify the `.env` file with appropriate values.

3. **Build and start the containers:**

   ```bash
   docker-compose up --build
   ```

   This will build and start all the services defined in the `docker-compose.yml` file.

## Services

### Django Application (`web`)

- **Build context:** `./compose/local/django/Dockerfile`
- **Command:** `/start`
- **Ports:** `8000:8000`
- **Volumes:**
  - `./web:/app` - Maps the local `web` folder to the `/app` directory in the container.
  - `static_volume:/app/assets` - Volume for static files.
  - `media_volume:/app/media` - Volume for media files.
- **Depends on:** `redis`, `db`

### PostgreSQL Database (`db`)

- **Image:** `postgres:14-alpine`
- **Environment Variables:**
  - `POSTGRES_DB`: `hello_django`
  - `POSTGRES_USER`: `hello_django`
  - `POSTGRES_PASSWORD`: `hello_django`
- **Ports:** `5431:5432`
- **Volumes:**
  - `postgres_data:/var/lib/postgresql/data/`

### Redis (`redis`)

- **Image:** `redis:7-alpine`

### Celery Worker (`celery_worker`)

- **Build context:** `./compose/local/django/Dockerfile`
- **Command:** `/start-celeryworker`
- **Depends on:** `redis`, `db`

### Celery Beat (`celery_beat`)

- **Build context:** `./compose/local/django/Dockerfile`
- **Command:** `/start-celerybeat`
- **Depends on:** `redis`, `db`

### Flower (`flower`)

- **Build context:** `./compose/local/django/Dockerfile`
- **Command:** `/start-flower`
- **Ports:** `5557:5555`
- **Depends on:** `redis`, `db`

### Nginx (`nginx`)

- **Build context:** `./nginx`
- **Ports:** `80:80`
- **Depends on:** `web`
- **Volumes:**
  - `static_volume:/app/assets`
  - `media_volume:/app/media`

## Accessing the Application

- **Django Application:** [http://localhost:8000](http://localhost:8000)
- **Flower Monitoring:** [http://localhost:5557](http://localhost:5557)
- **Nginx:** [http://localhost](http://localhost)

## Stopping the Containers

To stop the running containers, use:

```bash
docker-compose down
```

This will stop and remove all the containers defined in the `docker-compose.yml` file.

## Cleaning Up

To remove all volumes and images, you can use the following command:

```bash
docker-compose down --volumes --rmi all
```

## Troubleshooting

- **Check Logs:** Use `docker-compose logs` to view logs from all services.
- **Rebuild Containers:** If you face issues, try rebuilding the containers with `docker-compose up --build --force-recreate`.
