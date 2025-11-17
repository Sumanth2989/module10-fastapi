# FastAPI Secure User Module with CI/CD, Docker, and Testing

This project implements a secure FastAPI application with:

- A fully functional **SQLAlchemy User model**
- **Hashed passwords** using Passlib (bcrypt)
- **Pydantic schemas** for validation
- **Unit tests** + **Integration tests** with PostgreSQL
- A complete **CI/CD pipeline** using GitHub Actions
- **Automatic Docker image builds** pushed to Docker Hub

This project serves as the foundation for future modules and the final project.

---

## Features

### Secure User Model
- Unique `username` and `email`
- Hashed `password_hash` using bcrypt
- `created_at` timestamp
- SQLAlchemy ORM model

### Pydantic Schemas
- `UserCreate` — input validation for new users  
- `UserRead` — safe output schema (no password hash exposed)

### Password Hashing
- Secure hashing using `passlib[bcrypt]`
- Password verification helper

### Testing
- Unit tests for hashing and schema validation  
- Integration tests with real PostgreSQL (Testcontainers)  
- All tests run automatically in CI

### CI/CD Pipeline
- Runs tests on every push  
- Builds & pushes Docker image to Docker Hub when tests pass  
- Uses GitHub Actions + Docker Buildx

---


# Running Tests Locally

### 1. Start PostgreSQL (via Docker)

```bash
docker run --name test-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=test_db -p 5432:5432 -d postgres:15
```

### 2. Export the test database URL

```bash
export TEST_DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"
```

### 3. Run tests

```bash
pytest -q
```

---

# Running the Application with Docker

### 1. Pull the latest image

```bash
docker pull sumanthchand23/fastapi-secure-app:latest
```

### 2. Run the app

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/app_db" \
  sumanthchand23/fastapi-secure-app:latest
```

API runs at:

 http://localhost:8000

---

# Docker Hub Repository

Your Docker image is available here:
 **https://hub.docker.com/r/sumanthchand23/fastapi-secure-app**

Tags automatically pushed:

- `latest`
- Commit SHA tags

---

# CI/CD Workflow Overview

Your GitHub Actions pipeline performs:

1. Start PostgreSQL in services  
2. Install dependencies  
3. Run all tests  
4. Log in to Docker Hub using repo secrets  
5. Build + push Docker image with:
   - `latest`
   - commit SHA tag  
6. Only pushes if tests pass  

This ensures complete automated testing + deployment.

---

# Reflection

This project helped me understand how to build a secure API using FastAPI, SQLAlchemy, and Pydantic while following production-grade development practices. I learned how to implement proper password hashing, create validation schemas, and write both unit and integration tests.

The most challenging part was configuring GitHub Actions with PostgreSQL and Docker Hub authentication. After resolving token scopes and fixing image tagging in CI, I gained real experience in automated deployments, Docker, and CI/CD pipelines.

This workflow is now reusable for my future backend projects and the final project.

---
