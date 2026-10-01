# FPL data pipeline for a group of fantasy league managers who wants their data available during off season too because the fantasy premier league games data are usually not accessible when the season is over 

An automated ETL pipeline that extracts Fantasy Premier League standings, transforms the data, and loads it into PostgreSQL — orchestrated with Apache Airflow, containerized with Docker, and deployed on AWS EC2.

**Live demo:** http://13.60.35.33:8080 (Airflow UI — login: `admin` / see note below)

> Note: this is a portfolio project. The EC2 instance may be stopped between reviews to manage free-tier usage — reach out if the link isn't responding and I'll bring it back up.

## What it does

The pipeline runs daily but only produces new data during matchdays:

1. **Extracts** current standings from the Fantasy Premier League API for a specific classic league
2. **Transforms** the raw JSON into a clean, structured format (renamed columns, type validation, deduplication checks)
3. **Loads** the result into a PostgreSQL database, ready for downstream analysis or dashboarding
## Architecture

```
FPL API → Extract (Python/requests) → Transform (pandas) → Load (PostgreSQL)
                        ↑
              Orchestrated by Apache Airflow
                        ↑
         Containerized with Docker Compose
                        ↑
              Deployed on AWS EC2 (Ubuntu)
```

**Services running:**
- `postgres` — stores both Airflow's metadata and the pipeline's output data
- `airflow` — API server / web UI
- `airflow-scheduler` — triggers the DAG on schedule (`@daily`) because the might be premier league games within the weekdays and not only weekends
- `airflow-dag-processor` — parses and validates the DAG file

## Tech stack

- **Orchestration:** Apache Airflow 3.0
- **Language:** Python (pandas, requests)
- **Database:** PostgreSQL 17
- **Containerization:** Docker, Docker Compose
- **Cloud:** AWS EC2 (Ubuntu, t3.micro)
- **Version control:** Git/GitHub

## Notable engineering decisions & debugging

A few problems I diagnosed and fixed while building this:

- **Silent data-loss on container recreation** — Postgres had no named volume for its data directory, so every `docker compose down`/`up` cycle wiped the database. Fixed by adding a persistent named volume.
- **DAG showing "success" with zero tasks executed** — traced to a hardcoded `end_date` in the DAG definition that had already passed; Airflow was closing out runs without ever scheduling tasks against them.
- **Wrong data in the database** — the extract step was pointed at an incorrect FPL league ID and, separately, at the wrong API endpoint (a page URL instead of the JSON API endpoint), which surfaced as a `JSONDecodeError` when the response wasn't parseable JSON.
- **Database lock timeouts crashing the webserver** — root-caused to a stray heredoc syntax error in `init-db.sh` (a trailing space after the closing delimiter) that silently broke database initialization on certain restarts.
- **Cross-platform deployment issues** — case-sensitivity differences between Windows and Linux (`Docker-compose.yml` vs `docker-compose.yml`) broke the first deployment attempt on the EC2 instance.

## Running it locally

```bash
git clone https://github.com/thisizeru/fpl-data-pipeline.git
cd fpl-data-pipeline
cp .env.example .env   # fill in your own values
docker compose up -d
```

Airflow UI will be available at `http://localhost:8080`.
