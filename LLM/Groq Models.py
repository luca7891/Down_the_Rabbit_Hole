import requests
import os
import json
with open("groq_credentials.json") as f:
    credentials = json.load(f)

api_key = credentials.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.json())