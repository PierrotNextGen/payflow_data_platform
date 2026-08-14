

An end-to-end fintech transaction data platform built to simulate how payment transaction events can be ingested, streamed, transformed, quality-checked, and made available for downstream analytics.

Overview

PayFlow is a portfolio data engineering project built around a realistic financial transaction workflow.

The completed end-to-end implementation demonstrates the movement of transaction data through an event-driven ingestion layer, a lake-style processing architecture, and a PostgreSQL serving layer.

The project currently follows this flow:

FastAPI → Kafka → Bronze → Silver → Gold → PostgreSQL

The API generates transaction events containing customer, merchant, payment, transaction, and fraud-related attributes. Apache Kafka provides the event-streaming layer. Spark processes the data through Bronze and Silver stages before producing business-ready Gold datasets. The Gold datasets are then loaded into PostgreSQL for downstream consumption.

<img width="1024" height="1536" alt="ChatGPT Image Aug 14, 2026, 10_13_43 AM" src="https://github.com/user-attachments/assets/54c581df-aa3c-4ce1-b7c0-4d845e63b3a4" />

What the project demonstrates

1. Transaction API

FastAPI provides the transaction ingestion interface and generates realistic payment transactions containing information such as:

Customer information

Merchant information

Transaction amount

Currency

Payment method

Transaction status

Payment gateway

Fraud score

Fraud flag

Timestamp

The API provides the upstream source of transaction events for the streaming pipeline.

2. Event streaming with Kafka

Transaction events are published to an Apache Kafka topic:

transactions

Kafka decouples transaction generation from downstream processing and provides the event-driven backbone of the platform.

3. Bronze layer

The Bronze layer stores incoming transaction data in its raw form.

The purpose of Bronze is to preserve the incoming event data before applying downstream transformations.

Kafka
  ↓
Bronze

4. Silver layer

Apache Spark performs an incremental Bronze-to-Silver transformation.

The Silver layer:

Reads newly available Bronze data

Applies the transaction schema

Performs data transformations

Produces a cleaner transaction dataset

Uses a Spark checkpoint for incremental processing

Bronze
  ↓
Spark Structured Streaming
  ↓
Silver

5. Gold layer

The Gold transformation converts the Silver transaction data into business-oriented datasets.

The completed implementation produces:

Daily transactions

Provides daily transaction-level aggregates including:

Transaction count

Total transaction amount

Average transaction amount

Maximum transaction amount

Minimum transaction amount

Successful transactions

Failed transactions

Fraudulent transactions

Average fraud score

Merchant performance

Provides merchant-level performance metrics including:

Merchant identity and location

Merchant category

Transaction count

Total transaction amount

Average transaction amount

Successful transactions

Failed transactions

Fraudulent transactions

Average fraud score

Maximum transaction amount

Fraud analysis

Provides fraud-oriented aggregations across:

Transaction date

Merchant category

Payment method

Fraud status

Currency

Transaction count

Transaction amounts

Average fraud score

Maximum fraud score

Minimum fraud score

6. Data quality checks

The Gold transformation includes data quality checks before writing the final datasets.

The pipeline reports successful Gold data quality validation before completing the transformation.

7. PostgreSQL serving layer

The Gold datasets are loaded into PostgreSQL for downstream querying.

The current serving tables are:

daily_transactions
merchant_performance
fraud_analysis

Example:

SELECT *
FROM daily_transactions
ORDER BY transaction_date DESC;

Technology Stack

Technology

Purpose

Python

Application and data engineering code

FastAPI

Transaction API

PostgreSQL

Relational database and analytical serving layer

Apache Kafka

Event streaming

Apache Spark 4.0.1

Distributed data processing

Docker

Containerization

Docker Compose

Local infrastructure orchestration

Spark Structured Streaming

Incremental Bronze → Silver processing

Infrastructure

The local environment is containerized with Docker Compose.

The main services used by the completed pipeline are:

payflow-postgres
payflow-kafka
payflow-pipeline

The pipeline container runs the Spark-based transformations.

PostgreSQL is exposed locally on:

localhost:5433

Kafka is exposed locally on:

localhost:9092

Example transaction fields

The transaction model contains fields representing both payment and financial risk information, including:

transaction_id
customer_id
customer_name
customer_age
customer_occupation
customer_segment
customer_city
customer_province
issuing_bank
merchant_id
merchant_name
merchant_category
merchant_city
merchant_province
settlement_bank
amount
currency
payment_method
status
gateway
fraud_score
is_fraud
timestamp

Fraud detection

PayFlow includes rule-based fraud scoring as part of transaction generation.

The scoring logic considers transaction and behavioral attributes such as:

Transaction amount

Merchant risk

Customer risk

Payment method differences

Failed transactions

Additional randomized risk factors

The resulting score is stored with the transaction and used by the Gold fraud analysis dataset.

This is intentionally a rule-based demonstration, not a production fraud detection model.

Running the project

Start the infrastructure

docker compose up -d

Verify the containers:

docker ps

Expected services include:

payflow-postgres
payflow-kafka
payflow-pipeline

Run the transaction API

Activate the Python virtual environment and start FastAPI using the project's API entry point.

The API exposes interactive documentation through FastAPI/OpenAPI.

Once the API is running, transactions can be generated and published into the streaming workflow.

Inspect the pipeline

View pipeline logs with:

docker logs payflow-pipeline --tail 100

The completed pipeline reports the major stages:

Bronze -> Silver
Silver -> Gold
Gold -> PostgreSQL

Query PostgreSQL

Connect to the PayFlow database and inspect the analytical tables:

SELECT COUNT(*) FROM daily_transactions;

SELECT COUNT(*) FROM merchant_performance;

SELECT COUNT(*) FROM fraud_analysis;

Example:

SELECT *
FROM daily_transactions
ORDER BY transaction_date DESC;

Project outcomes

The completed implementation demonstrates an end-to-end path from transaction generation to analytical serving:

Transaction
    ↓
FastAPI
    ↓
Kafka
    ↓
Bronze
    ↓
Spark
    ↓
Silver
    ↓
Spark
    ↓
Gold
    ↓
PostgreSQL

This provides a practical demonstration of:

Event-driven architecture

Streaming ingestion

Incremental data processing

Medallion architecture

Spark transformations

Data quality validation

Financial transaction modeling

Fraud-oriented analytics

Containerized data infrastructure

Current status

Completed: End-to-end local data platform.

The current implementation successfully demonstrates the complete transaction data flow from the API/event layer through Kafka, Bronze, Silver, Gold, and PostgreSQL.

Future development

The current repository is intentionally being treated as the completed end-to-end foundation.

Future development will evolve PayFlow into a more production-oriented fintech platform, with the transaction API becoming the primary product and the data platform becoming a downstream consumer.

Planned technologies for the next stage include:

Databricks

Delta Lake

Kafka

Spark

dbt

Production-grade API authentication

Idempotency

Automated testing

Monitoring

Cloud deployment

Real-time financial analytics

These are future extensions and are not presented as part of the completed implementation documented above.

Portfolio context

PayFlow was designed as a practical demonstration of how a fintech application can generate financial transaction events and how a modern data engineering platform can process those events for analytics.

The project focuses on the complete engineering flow rather than a single isolated technology:

Application → Event Streaming → Data Lake → Transformation → Analytics Serving

Author

Built as a portfolio project focused on fintech, backend engineering, and data engineering.




