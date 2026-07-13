# Docker Flask, Redis and Nginx Application

## Project Overview

This project demonstrates how to containerise a Flask web application using Docker and manage multiple services with Docker Compose. The application uses Redis as a database to store a page visit counter, while Nginx acts as a reverse proxy, forwarding incoming requests to the Flask application.

---

## Technologies Used

- Docker
- Docker Compose
- Flask
- Redis
- Nginx
- Python

---

## Project Architecture

```
Browser
    │
    ▼
Nginx (Port 80)
    │
    ▼
Flask Web Application (Port 5002)
    │
    ▼
Redis Database (Port 6379)
```

---

## Docker

Docker allows applications to be packaged together with all of their dependencies into an image. An image acts as a blueprint from which containers are created. This ensures the application runs consistently regardless of the environment.

For this project I created a Docker image for the Flask application using a Dockerfile. The Dockerfile installs Python, Flask and Redis, copies the application code into the image and specifies the command used to start the application.

---

## Containers

Each service in the application runs inside its own container.

The project contains three containers:

- Flask container – runs the Python web application.
- Redis container – stores the page visit count.
- Nginx container – receives HTTP requests and forwards them to the Flask application.
.

---

## Redis Database

Redis is used as an in-memory database to store the number of visits to the `/count` endpoint.

Each time the page is accessed, Flask executes:

```python
visit_count = r.incr("visits")
```

Redis automatically increments the value stored under the key `visits` and returns the updated count.

To make the Redis data persistent, Append Only File (AOF) persistence was enabled using:

```yaml
command: redis-server --appendonly yes
```

A Docker volume was also created:

```yaml
volumes:
  - redis-data:/data
```

This stores the Redis data outside the container so it is preserved even if the container is removed.

---

## Docker Compose

Docker Compose was used to manage all three services together.

Instead of manually creating containers and networks using multiple `docker run` commands, Docker Compose automatically:

- Builds the Flask image
- Creates a Docker network
- Starts the Redis container
- Starts the Flask container
- Starts the Nginx container
- Connects all containers together

Because Docker Compose creates an internal network automatically, containers communicate using their service names.

For example:

- Flask connects to Redis using `redis`
- Nginx forwards requests to Flask using `web`

---

## Nginx Reverse Proxy

Nginx acts as the application's entry point.

The browser communicates with Nginx, and Nginx forwards incoming requests to the Flask application.

The Nginx configuration file is mounted into the container using:

```yaml
volumes:
  - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

The `./` refers to the current project directory. This replaces the default Nginx configuration inside the container with the custom configuration stored locally.

The `:ro` option mounts the file as read-only, preventing the container from modifying the configuration.

---

## Networking

Docker Compose automatically creates a private network for the application.

This allows containers to communicate using their service names:

- `web`
- `redis`
- `nginx`

The Flask application is not exposed directly to the host machine. Instead, it uses:

```yaml
expose:
  - "5002"
```

This makes port 5002 available only to other containers on the Docker network.

Nginx is the only service exposed externally using:

```yaml
ports:
  - "5002:80"
```

This maps port **5002** on the host machine to port **80** inside the Nginx container.

Users access the application by visiting:

```
http://localhost:5002
```

---

## Running the Project

Build and start all services:

```bash
docker compose up --build
```

Stop the application:

```bash
docker compose down
```

---

## What I Learned

During this project I learned how to:

- Build Docker images using a Dockerfile.
- Run applications inside Docker containers.
- Use Redis as a persistent database.
- Configure Docker Compose to manage multiple services.
- Allow containers to communicate over an automatically created Docker network.
- Use environment variables to configure container communication.
- Configure Nginx as a reverse proxy.
- Use bind mounts and Docker volumes for configuration files and persistent data.