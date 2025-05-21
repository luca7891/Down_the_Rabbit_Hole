import json
from groq import Groq

# Load the API key from a local JSON file
with open("groq_credentials.json") as f:
    credentials = json.load(f)

api_key = credentials.get("GROQ_API_KEY")

# Initialize the Groq client
client = Groq(api_key=api_key)

# Define your model names
model = "llama-3.3-70b-versatile"

# Function to get response from LLaMA model
def get_responsellama(prompt, model=model, temperature=0.2, max_tokens=256):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content
