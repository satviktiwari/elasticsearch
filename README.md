🌍 Logstash API Data Ingestion to Elasticsearch
This project demonstrates how to use Logstash to ingest data from a public REST API (https://restcountries.com/v3.1/all) and index it into Elasticsearch for search and analysis.

📦 Project Structure
bash
Copy
Edit
.
├── restcountries-to-es.conf   # Logstash config file
└── README.md                  # This documentation
🚀 Features
Polls country data from the REST Countries API

Extracts and transforms key fields: country name, code, and region

Ingests structured data into Elasticsearch index

Scheduled every 10 minutes

Logs documents to console for debugging

🔧 Prerequisites
Elasticsearch (Running locally or remotely)

Logstash installed

Internet access to hit the public REST API

⚙️ Configuration Details
Logstash Input (HTTP Poller):

Endpoint: https://restcountries.com/v3.1/all

Method: GET

Schedule: Every 10 minutes

Filter:

Splits the array of countries

Extracts and flattens fields:

country: Common country name

country_code: 2-letter country code (cca2)

region: Geographic region

Adds ingestion timestamp

Output:

Elasticsearch index: restcountries-index

Also prints data to console for debugging

📄 restcountries-to-es.conf
conf
Copy
Edit
input {
  http_poller {
    urls => {
      countries => {
        method => get
        url => "https://restcountries.com/v3.1/all"
      }
    }
    request_timeout => 60
    schedule => { every => "10m" }
    codec => "json"
    metadata_target => "http_poller_metadata"
  }
}

filter {
  split {
    field => "message"
  }

  mutate {
    rename => {
      "[message][name][common]" => "country"
      "[message][region]" => "region"
      "[message][cca2]" => "country_code"
    }

    add_field => {
      "timestamp" => "%{@timestamp}"
    }
  }
}

output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "restcountries-index"
  }

  stdout {
    codec => rubydebug
  }
}
▶️ How to Run
Ensure Elasticsearch is running:

bash
Copy
Edit
curl http://localhost:9200
Start Logstash with the config:

bash
Copy
Edit
bin/logstash -f restcountries-to-es.conf
Verify data in Elasticsearch:

bash
Copy
Edit
curl http://localhost:9200/restcountries-index/_search?pretty
📊 Sample Output in Elasticsearch
json
Copy
Edit
{
  "country": "India",
  "country_code": "IN",
  "region": "Asia",
  "timestamp": "2025-05-11T15:30:00.123Z"
}
🧪 Notes
You can enrich the data further by adding more fields from the API (e.g., population, subregion, timezones).

Adjust polling frequency in the schedule field as needed.

To scale ingestion for larger data, consider using batching and tuning Logstash performance settings.

📜 License
This project uses open public data from REST Countries and is open-source under the MIT license.

Would you like to package this into a GitHub-ready structure or include Docker support?







You said:
generate the .md file


ChatGPT said:
Sure! Here's the full README.md file content you can save directly:

markdown
Copy
Edit
# 🌍 Logstash API Data Ingestion to Elasticsearch

This project demonstrates how to use **Logstash** to ingest data from a public REST API (`https://restcountries.com/v3.1/all`) and index it into **Elasticsearch** for search and analysis.

---

## 📦 Project Structure

.
├── restcountries-to-es.conf # Logstash config file
└── README.md # This documentation

yaml
Copy
Edit

---

## 🚀 Features

- Polls country data from the REST Countries API
- Extracts and transforms key fields: country name, code, and region
- Ingests structured data into Elasticsearch index
- Scheduled every 10 minutes
- Logs documents to console for debugging

---

## 🔧 Prerequisites

- [Elasticsearch](https://www.elastic.co/downloads/elasticsearch) (Running locally or remotely)
- [Logstash](https://www.elastic.co/downloads/logstash) installed
- Internet access to hit the public REST API

---

## ⚙️ Configuration Details

**Logstash Input (HTTP Poller):**
- Endpoint: `https://restcountries.com/v3.1/all`
- Method: `GET`
- Schedule: Every 10 minutes

**Filter:**
- Splits the array of countries
- Extracts and flattens fields:
  - `country`: Common country name
  - `country_code`: 2-letter country code (cca2)
  - `region`: Geographic region
- Adds ingestion timestamp

**Output:**
- Elasticsearch index: `restcountries-index`
- Also prints data to console for debugging

---

## 📄 `restcountries-to-es.conf`

```conf
input {
  http_poller {
    urls => {
      countries => {
        method => get
        url => "https://restcountries.com/v3.1/all"
      }
    }
    request_timeout => 60
    schedule => { every => "10m" }
    codec => "json"
    metadata_target => "http_poller_metadata"
  }
}

filter {
  split {
    field => "message"
  }

  mutate {
    rename => {
      "[message][name][common]" => "country"
      "[message][region]" => "region"
      "[message][cca2]" => "country_code"
    }

    add_field => {
      "timestamp" => "%{@timestamp}"
    }
  }
}

output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "restcountries-index"
  }

  stdout {
    codec => rubydebug
  }
}
▶️ How to Run
Ensure Elasticsearch is running:

bash
Copy
Edit
curl http://localhost:9200
Start Logstash with the config:

bash
Copy
Edit
bin/logstash -f restcountries-to-es.conf
Verify data in Elasticsearch:

bash
Copy
Edit
curl http://localhost:9200/restcountries-index/_search?pretty
📊 Sample Output in Elasticsearch
json
Copy
Edit
{
  "country": "India",
  "country_code": "IN",
  "region": "Asia",
  "timestamp": "2025-05-11T15:30:00.123Z"
}
🧪 Notes
You can enrich the data further by adding more fields from the API (e.g., population, subregion, timezones).

Adjust polling frequency in the schedule field as needed.

To scale ingestion for larger data, consider using batching and tuning Logstash performance settings.

📜 License
This project uses open public data from REST Countries and is open-source under the MIT license.
