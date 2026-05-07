# Risk Reporting Suite

## Project Overview

Risk Reporting Suite is a backend application built using Spring Boot for managing and tracking organizational risks.

The system provides:
- Risk management APIs
- JWT authentication
- Swagger API documentation
- MySQL database integration
- Redis integration
- Dockerized deployment

---

## Tech Stack

- Java 17
- Spring Boot 3
- Spring Security
- JWT Authentication
- MySQL
- Redis
- Docker
- Swagger/OpenAPI
- Maven

---

## ASCII Architecture Diagram

```text
                 +-------------------+
                 |   Swagger UI      |
                 |  localhost:8080   |
                 +---------+---------+
                           |
                           v
                +----------+----------+
                |   Spring Boot App   |
                |   Risk Reporting    |
                +----------+----------+
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
 +--------+--------+              +---------+--------+
 |     MySQL DB    |              |      Redis       |
 |     riskdb      |              |   Cache Layer    |
 +-----------------+              +------------------+
```

---

## Features

- Create risks
- Fetch risks
- Update risks
- Delete risks
- JWT authentication
- Swagger API documentation
- Docker support
- Redis integration
- Data seeder support

---

## Prerequisites

Install the following before running the project:

- Java 17
- Maven
- Docker Desktop
- Git

---

## Setup Steps

### 1. Clone Repository

```bash
git clone <repository-url>
```

---

### 2. Navigate to Project

```bash
cd risk-reporting-suite
```

---

### 3. Start Docker Containers

```bash
docker compose up --build
```

---

### 4. Open Swagger UI

```text
http://localhost:8080/swagger-ui/index.html
```

---

## Environment Configuration

### .env.example

| Variable | Description |
|---|---|
| DB_HOST | MySQL host |
| DB_PORT | MySQL port |
| DB_NAME | Database name |
| DB_USER | Database username |
| DB_PASSWORD | Database password |
| JWT_SECRET | JWT secret key |
| REDIS_HOST | Redis host |
| REDIS_PORT | Redis port |

---

## Docker Services

| Service | Port |
|---|---|
| Spring Boot App | 8080 |
| MySQL | 3307 |
| Redis | 6379 |

---

## API Testing

Swagger UI:

```text
http://localhost:8080/swagger-ui/index.html
```

---

## Author

Java Developer 1 Internship Project