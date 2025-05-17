import requests
import json

# List of all your 10 metric endpoints on Flask app
metric_endpoints = [
    "http://localhost:5002/metrics/logs_per_day",
    "http://localhost:5002/metrics/logs_per_level",
    "http://localhost:5002/metrics/error_count",
    "http://localhost:5002/metrics/warning_count",
    "http://localhost:5002/metrics/info_count",
    "http://localhost:5002/metrics/debug_count",
    "http://localhost:5002/metrics/critical_count",
    "http://localhost:5002/metrics/logs_per_hour",
    "http://localhost:5002/metrics/top_error_messages",
    "http://localhost:5002/metrics/top_users"
]

llm_api_url = "http://localhost:11434/api/generate"

def create_prompt(endpoint, data):
    # Customize prompt based on the endpoint and the data format
    prompt = f"Summarize the metric for endpoint '{endpoint}':\n"

    if isinstance(data, dict) and "buckets" in data:
        # Most ES agg responses have buckets
        for bucket in data["buckets"]:
            key = bucket.get("key_as_string") or bucket.get("key") or "N/A"
            count = bucket.get("doc_count", 0)
            prompt += f"{key}: {count}\n"
    elif isinstance(data, dict):
        # Fallback for dict data without buckets
        for k, v in data.items():
            prompt += f"{k}: {v}\n"
    elif isinstance(data, list):
        # If data is a list of items
        for item in data:
            prompt += json.dumps(item) + "\n"
    else:
        # Generic string or unknown format
        prompt += str(data)

    return prompt

def get_metric_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def send_to_llm(prompt):
    payload = {
        "model": "gemma:2b",
        "prompt": prompt,
    }

    response = requests.post(llm_api_url, json=payload, stream=True)
    summary = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                summary += data.get("response", "")
                if data.get("done", False):
                    break
            except Exception:
                continue
    return summary

def main():
    for endpoint in metric_endpoints:
        print(f"\nFetching data from: {endpoint}")
        try:
            data = get_metric_data(endpoint)
        except Exception as e:
            print(f"Failed to fetch data from {endpoint}: {e}")
            continue

        prompt = create_prompt(endpoint, data)
        print(f"\nSending prompt to LLM:\n{prompt}")

        try:
            summary = send_to_llm(prompt)
            print(f"\nLLM Summary for {endpoint}:\n{summary}\n{'-'*50}")
        except Exception as e:
            print(f"Failed to get summary from LLM for {endpoint}: {e}")

if __name__ == "__main__":
    main()
