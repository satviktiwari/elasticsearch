import requests
import json

response = requests.post("http://localhost:11434/api/generate", 
                         json={"model": "gemma:2b",
                               "prompt": "Explain what this error log means: [ERROR] Timeout after 10 seconds trying to reach Elasticsearch."}, 
                               stream=True)

for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line)
            print(data["response"], end="", flush=True)
        except Exception as e:
            print("Invalid chunk:", line)