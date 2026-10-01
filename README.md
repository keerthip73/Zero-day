# ZeroGuard AI

ZeroGuard AI is an academic, defensive cybersecurity project that detects unusual network-flow behavior and helps an analyst review the resulting events and alerts. It combines an Isolation Forest model, a FastAPI inference service, a Spring Boot API, and a React dashboard in one local development environment.

> ZeroGuard identifies statistical anomalies; it does not prove that an event is a zero-day attack. Predictions should be treated as investigation leads.

## Features

- Network-flow anomaly scoring with an Isolation Forest baseline
- Risk scores, severity classification, confidence, and human-readable reasons
- JWT-based registration, login, and protected API endpoints
- Event ingestion, batch ingestion, alert creation, analyst notes, and alert status updates
- Dashboard summaries, recent risk charts, event monitoring, and model information
- Safe synthetic demo events for repeatable classroom demonstrations
- PostgreSQL for the Docker environment and in-memory H2 for lightweight local development
- Docker Compose orchestration and GitHub Actions checks

## Architecture

```text
Browser
  |
  v
React + TypeScript dashboard (5173)
  |
  v
Spring Boot REST API (8080) ----> PostgreSQL / H2
  |
  v
FastAPI ML service (8000) ----> Isolation Forest model
```

The backend validates and stores each event, requests a prediction from the ML service, stores the detection result, and creates an alert when the configured risk threshold is reached. More detail is available in [docs/architecture.md](docs/architecture.md).

## Technology Stack

| Area | Technologies |
| --- | --- |
| Frontend | React 19, TypeScript, Vite, React Router, Axios, Recharts |
| Backend | Java 21, Spring Boot 3, Spring Security, Spring Data JPA, JWT, Maven |
| ML service | Python, FastAPI, Pandas, NumPy, Scikit-learn, Joblib |
| Database | PostgreSQL 16 in Docker; H2 for local development |
| Tooling | Docker Compose, GitHub Actions |

## Repository Layout

```text
zeroguard-ai/
|-- frontend/          React analyst dashboard
|-- backend/           Spring Boot API and persistence layer
|-- ml-service/        FastAPI inference service and ML modules
|-- data/              Demo, raw, and processed dataset directories
|-- models/            Generated model artifacts (not committed)
|-- scripts/           Data, training, simulation, and run scripts
|-- docs/              Architecture, dataset, modeling, and project notes
|-- docker-compose.yml
`-- .env.example
```

## Quick Start with Docker

### Requirements

- Docker Desktop with the Linux engine running
- WSL 2 and hardware virtualization enabled on Windows

Open PowerShell in the repository root:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Open `http://localhost:5173`, create an account, sign in, and select **Run Demo Events**. The other services are available at:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8080`
- ML service: `http://localhost:8000`
- ML API documentation: `http://localhost:8000/docs`

Stop the application with `Ctrl+C`, then run:

```powershell
docker compose down
```

To also delete the local PostgreSQL volume, use `docker compose down -v`.

## Run Locally Without Docker

### Requirements

- Python 3.11 or newer
- Java 21
- Maven 3.9 or the Maven installation bundled with IntelliJ IDEA
- Node.js 20 or newer with npm

Use three PowerShell windows and keep each process running.

### 1. ML service

First-time setup:

```powershell
python -m venv ml-service\.venv
.\ml-service\.venv\Scripts\python.exe -m pip install -r ml-service\requirements.txt
```

Prepare the demo data, train the baseline model, and start FastAPI:

```powershell
.\scripts\run_ml_service.ps1
```

### 2. Backend

In a second PowerShell window:

```powershell
.\scripts\run_backend_local.ps1
```

The local Spring profile uses an in-memory H2 database, so PostgreSQL is not required. Data is reset whenever the backend is restarted.

### 3. Frontend

In a third PowerShell window:

```powershell
.\scripts\run_frontend.ps1
```

Open `http://localhost:5173`, register an analyst account, and log in.

## API Overview

Authentication endpoints:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

Protected event and analyst endpoints:

- `POST /api/events`
- `POST /api/events/batch`
- `GET /api/events`
- `GET /api/events/{id}`
- `GET /api/alerts`
- `PATCH /api/alerts/{id}/status`
- `POST /api/events/{id}/notes`
- `GET /api/dashboard/summary`

ML service endpoints:

- `GET /health`
- `GET /model/info`
- `POST /predict`
- `POST /predict/batch`

Protected backend requests require `Authorization: Bearer <token>`. A token is returned by the login endpoint and is managed automatically by the frontend.

## Data and Model

The included file at [data/demo/security_events_sample.csv](data/demo/security_events_sample.csv) is a small, safe synthetic dataset intended only to demonstrate the pipeline. It is not suitable for reporting real-world model accuracy.

The preprocessing pipeline validates the flow schema, derives model features, splits the data, and writes generated files under `data/processed`. Training writes model artifacts under `models`. Both generated directories are excluded from Git.

For dataset guidance and model limitations, see:

- [Dataset guide](docs/dataset.md)
- [Preprocessing guide](docs/preprocessing.md)
- [Modeling notes](docs/modeling.md)

## Tests

Run ML tests:

```powershell
.\ml-service\.venv\Scripts\python.exe -m unittest discover -s ml-service\tests
```

Run backend tests:

```powershell
mvn -f backend\pom.xml test
```

Run frontend tests and build:

```powershell
Set-Location frontend
npm install
npm test
npm run build
```

## Configuration

Copy `.env.example` to `.env` for Docker configuration. Important settings include database credentials, the JWT signing secret, service ports, the CORS origin, and the alert risk threshold.

Never commit `.env`, private keys, production credentials, raw packet payloads, generated datasets, or trained model artifacts. The repository's `.gitignore` excludes these local files.

## Academic Scope

This repository is intended for coursework, portfolio demonstrations, and defensive security learning. It does not contain malware, exploit code, destructive actions, credential attacks, or offensive scanning features. All demo traffic is synthetic.

## Future Improvements

- Train and compare an autoencoder on a full public intrusion-detection dataset
- Add model version management and drift monitoring
- Expand backend and frontend automated test coverage
- Add richer alert assignment and investigation workflows
- Measure precision, recall, F1, and false-positive rate on a held-out real dataset

## License

This project is currently provided for academic and portfolio use. Add a formal open-source license before accepting external contributions or redistribution.
