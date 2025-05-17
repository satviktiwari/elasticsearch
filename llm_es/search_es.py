from flask import Flask, jsonify
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "app-logs"

# 1. Count total logs
@app.route("/metrics/total_logs", methods=["GET"])
def total_logs():
    result = es.count(index=INDEX_NAME)
    return jsonify({"total_logs": result['count']})

# 2. Logs count per level
@app.route("/metrics/logs_per_level", methods=["GET"])
def logs_per_level():
    body = {
        "size": 0,
        "aggs": {
            "levels": {
                "terms": {"field": "level.keyword"}
            }
        }
    }
    result = es.search(index=INDEX_NAME, body=body)
    return jsonify({bucket['key']: bucket['doc_count'] for bucket in result['aggregations']['levels']['buckets']})

# 3. Top 5 most frequent messages
@app.route("/metrics/top_messages", methods=["GET"])
def top_messages():
    body = {
        "size": 0,
        "aggs": {
            "top_messages": {
                "terms": {"field": "message.keyword", "size": 5}
            }
        }
    }
    result = es.search(index=INDEX_NAME, body=body)
    return jsonify({bucket['key']: bucket['doc_count'] for bucket in result['aggregations']['top_messages']['buckets']})

# 4. Logs count in last 1 hour
@app.route("/metrics/logs_last_hour", methods=["GET"])
def logs_last_hour():
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    body = {
        "query": {
            "range": {
                "timestamp": {
                    "gte": one_hour_ago.isoformat(),
                    "lte": now.isoformat()
                }
            }
        }
    }
    result = es.count(index=INDEX_NAME, body=body)
    return jsonify({"logs_last_hour": result['count']})

# 5. Latest error log
@app.route("/metrics/latest_error", methods=["GET"])
def latest_error():
    body = {
        "size": 1,
        "sort": [{"timestamp": {"order": "desc"}}],
        "query": {
            "match": {"level": "ERROR"}
        }
    }
    result = es.search(index=INDEX_NAME, body=body)
    if result['hits']['hits']:
        return jsonify(result['hits']['hits'][0]['_source'])
    return jsonify({"message": "No error logs found."})

# 6. Count logs per day (last 7 days)
@app.route("/metrics/logs_per_day", methods=["GET"])
def logs_per_day():
    body = {
        "size": 0,
        "aggs": {
            "logs_by_day": {
                "date_histogram": {
                    "field": "timestamp",
                    "calendar_interval": "day"
                }
            }
        }
    }
    result = es.search(index=INDEX_NAME, body=body)
    return jsonify({bucket['key_as_string']: bucket['doc_count'] for bucket in result['aggregations']['logs_by_day']['buckets']})

# 7. Count of critical errors
@app.route("/metrics/critical_errors", methods=["GET"])
def critical_errors():
    body = {
        "query": {
            "match": {"level": "CRITICAL"}
        }
    }
    result = es.count(index=INDEX_NAME, body=body)
    return jsonify({"critical_errors": result['count']})

# 8. Keyword-based search
@app.route("/metrics/search/<keyword>", methods=["GET"])
def search_keyword(keyword):
    body = {
        "query": {
            "match": {
                "message": keyword
            }
        }
    }
    result = es.search(index=INDEX_NAME, body=body, size=10)
    return jsonify([hit['_source'] for hit in result['hits']['hits']])

# 9. Logs per minute (last 60 minutes)
@app.route("/metrics/logs_per_minute", methods=["GET"])
def logs_per_minute():
    body = {
        "size": 0,
        "aggs": {
            "logs_by_minute": {
                "date_histogram": {
                    "field": "timestamp",
                    "calendar_interval": "minute"
                }
            }
        }
    }
    result = es.search(index=INDEX_NAME, body=body)
    return jsonify({bucket['key_as_string']: bucket['doc_count'] for bucket in result['aggregations']['logs_by_minute']['buckets']})

# 10. Get random log
@app.route("/metrics/random_log", methods=["GET"])
def random_log():
    body = {
        "size": 1,
        "query": {"function_score": {"random_score": {}}}
    }
    result = es.search(index=INDEX_NAME, body=body)
    if result['hits']['hits']:
        return jsonify(result['hits']['hits'][0]['_source'])
    return jsonify({"message": "No logs found."})

# Start Flask app
if __name__ == "__main__":
    app.run(port=5002, debug=True)
