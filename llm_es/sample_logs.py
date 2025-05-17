from elasticsearch import Elasticsearch, helpers
import random
import time
import uuid

es = Elasticsearch("http://localhost:9200")

# Log level and message pool
log_levels = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
log_messages = [
    "User logged in successfully.",
    "Fetching data from Elasticsearch.",
    "Timeout after 10 seconds trying to reach Elasticsearch.",
    "Connection refused by database.",
    "Disk space running low.",
    "Null pointer exception at line 42.",
    "Memory usage exceeded threshold.",
    "Authentication token expired.",
    "Rate limit exceeded for user.",
    "File not found: config.yaml"
]

def generate_log():
    return {
        "_index": "app-logs",
        "_id": str(uuid.uuid4()),
        "_source": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": random.choice(log_levels),
            "message": random.choice(log_messages)
        }
    }

# Create 10,000 log events
logs = (generate_log() for _ in range(50_000))

# Bulk insert into Elasticsearch
helpers.bulk(es, logs)

print("✅ Inserted 50,000 logs into Elasticsearch index 'app-logs'")
