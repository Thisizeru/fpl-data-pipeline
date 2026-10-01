#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE fpl_db;
    GRANT ALL PRIVILEGES ON DATABASE fpl_db TO airflow;
EOSQL