# Elasticsearch Logs Analytics with LLM Summarization

This project demonstrates an end-to-end pipeline for generating random logs, ingesting them into Elasticsearch, querying various log metrics through a Flask API, and summarizing those metrics using a local LLM model (gemma:2b) with streaming responses.

## Table of Contents

- [Project Overview](#project-overview)
- [Components](#components)
- [Setup and Installation](#setup-and-installation)
- [Generating and Ingesting Logs](#generating-and-ingesting-logs)
- [Flask API for Log Metrics](#flask-api-for-log-metrics)
- [Querying and Summarizing with LLM](#querying-and-summarizing-with-llm)
- [Usage](#usage)
- [Example cURL / Postman Requests](#example-curl--postman-requests)
- [Notes](#notes)
- [Future Enhancements](#future-enhancements)

## Project Overview

The purpose of this project is to simulate logging data ingestion and analysis, coupled with advanced AI-powered summarization. It showcases:

- Generation of 100,000 random log events with varying log levels and messages
- Bulk ingestion of log data into Elasticsearch
- A Flask-based REST API exposing 10 endpoints for different log metrics via Elasticsearch queries
- Integration with a local LLM (gemma:2b) to generate human-readable summaries of metric data, streamed via API
- Streaming response handling and prompt crafting for effective summarization

## Components

- **Log Generator and Elasticsearch Ingestion Script:**  
  Generates 100k synthetic logs and bulk loads them into Elasticsearch.

- **Flask Metrics API:**  
  Provides multiple endpoints to query log metrics such as logs per day, logs per level, error counts, warnings, and more.

- **LLM Summarization Client:**  
  Fetches metrics from Flask endpoints, sends them to the gemma:2b model API, and streams back text summaries.

## Setup and Installation

### Prerequisites

- Python 3.8+
- Elasticsearch 7.x or 8.x running locally or accessible remotely
- Local LLM API (gemma:2b) running on `http://localhost:11434/api/generate` (or update accordingly)
- Flask for the REST API

### Install Python dependencies

pip install flask requests elasticsearch

text

### Run Elasticsearch

Make sure Elasticsearch is running and accessible on `localhost:9200` or update connection details in scripts.

## Generating and Ingesting Logs

Use the provided Python script to generate 100,000 random logs and bulk insert into Elasticsearch index named `app-logs`: generate_logs.py

## Flask API for Log Metrics

The Flask app exposes 10 endpoints to fetch different log metrics from Elasticsearch using aggregation queries.

Example endpoints include:

- `/metrics/logs_per_day`
- `/metrics/logs_per_level`
- `/metrics/error_count`
- `/metrics/warning_count`
- `/metrics/info_count`
- `/metrics/debug_count`
- `/metrics/critical_count`
- `/metrics/logs_per_hour`
- `/metrics/top_error_messages`
- `/metrics/top_users`

Run the Flask app (e.g., on port 5002):

python flask_metrics_api.py

text

Each endpoint returns JSON with aggregation results from Elasticsearch.

## Querying and Summarizing with LLM

A Python client script queries all Flask metric endpoints, formats the data into prompts, sends those prompts to the gemma:2b local LLM API, and streams back the text summary.

Key features:

- Handles streaming JSON chunks from LLM API
- Converts Elasticsearch aggregation buckets into readable text prompts
- Prints final summarized output for each metric

Example snippet:

import requests
import json

Example prompt creation from metric data
prompt = "Summarize logs per day metric:\n"
for bucket in data["buckets"]:
prompt += f"{bucket['key_as_string']}: {bucket['doc_count']}\n"

Send to LLM streaming API
response = requests.post(llm_api_url, json={"model": "gemma:2b", "prompt": prompt}, stream=True)
for line in response.iter_lines():
if line:
chunk = json.loads(line)
print(chunk.get("response", ""), end="", flush=True)

text

## Usage

1. Run Elasticsearch and ensure it's accessible.
2. Generate and ingest logs using the provided ingestion script.
3. Start the Flask metrics API server.
4. Run the summarization client to fetch metrics and generate LLM summaries.

## Example cURL / Postman Requests

Fetch logs per day metric:

curl -X GET "http://localhost:5002/metrics/logs_per_day"


Fetch logs per level metric:

curl -X GET "http://localhost:5002/metrics/logs_per_level"


Send prompt to LLM API:

curl -X POST "http://localhost:11434/api/generate"
-H "Content-Type: application/json"
-d '{"model":"gemma:2b","prompt":"Summarize logs per day..."}' --no-buffer

text

## Notes

- Elasticsearch fields used for aggregation (e.g., `timestamp`) need to be keyword or date types with `doc_values` enabled for aggregation support.
- The LLM API is expected to provide streaming JSON responses chunked by tokens.
- Prompts are crafted to ensure meaningful summarization by the LLM.
- Bulk ingestion uses `helpers.bulk()` from the Elasticsearch Python client for efficiency.

## Future Enhancements

- Add user authentication to the Flask API
- Support filtered queries and pagination for large metrics
- Enhance LLM prompt engineering for richer insights
- Add frontend UI dashboard to visualize metrics and AI summaries
- Integrate alerting/notifications based on metric thresholds

---

If you have any questions or need help extending this project, feel free to ask.
