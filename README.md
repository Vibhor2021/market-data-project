# Market Data Pipeline

## Architecture

FastAPI API
    ↓
ETL Pipeline
    ↓
PostgreSQL

## Features

- Synthetic Market Data API
- Fault Injection (5%)
- Pydantic Validation
- VWAP Calculation
- Outlier Detection
- PostgreSQL Storage
- Structured Logging
- Dockerized Deployment

## Setup

docker compose up --build

## API Endpoint

GET /v1/market-data

## Database Schema

market_data

Columns:
- instrument_id
- price
- volume
- timestamp
- vwap
- is_outlier

## Scaling

For 1 billion events/day:

FastAPI
↓
Kafka
↓
Spark Streaming
↓
Data Lake
↓
Data Warehouse

## Monitoring

- Health Check APIs
- Prometheus
- Grafana
- Structured Logs

## Recovery / Idempotency

- Unique Constraint
- Database Transactions
- Retry Mechanism
- Checkpointing